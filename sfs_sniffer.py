"""
SmartFoxServer 1.x (legacy) compatible server, matching the exact protocol
used by it.gotoandplay.smartfoxserver.SmartFoxClient / SysHandler as
decompiled from LSWIII.swf.

Wire format: <msg t='sys'><body action='X' r='ROOMID'>...</body></msg>\x00

Implements: verChk, login, getRmList (auto-sent after login), createRoom,
joinRoom, setUvars, setRvars, pubMsg, leaveRoom, disconnect.

Run:
    python3 sfs_server.py
"""

import asyncio
import xml.etree.ElementTree as ET
import itertools

HOST = "0.0.0.0"
PORT = 9339

next_user_id = itertools.count(1)


class Room:
    def __init__(self, room_id, name, max_users=12):
        self.id = room_id
        self.name = name
        self.max_users = max_users
        self.users = {}       # user_id -> User
        self.variables = {}   # name -> (value, type)


class User:
    def __init__(self, user_id, writer):
        self.id = user_id
        self.writer = writer
        self.name = f"Galaxy{user_id}"
        self.room = None
        self.player_id = -1
        self.variables = {}   # name -> (value, type)


rooms_by_name = {}
rooms_by_id = {}
next_room_id = itertools.count(1)
users = {}


def ensure_lobby():
    if "Lobby" in rooms_by_name:
        return rooms_by_name["Lobby"]
    rid = next(next_room_id)
    room = Room(rid, "Lobby", 100)
    rooms_by_name["Lobby"] = room
    rooms_by_id[rid] = room
    print(f"[room] created 'Lobby' (id={rid})")
    return room


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace("'", "&apos;").replace('"', "&quot;"))


async def send(user, msg):
    try:
        user.writer.write(msg.encode("utf-8") + b"\x00")
        await user.writer.drain()
        print(f"[>{user.id}] {msg}")
    except Exception as e:
        print(f"[!] send to {user.id} failed: {e}")


async def broadcast(room, msg, exclude=None):
    for uid, u in list(room.users.items()):
        if uid != exclude:
            await send(u, msg)


def vars_xml(variables: dict):
    parts = "".join(
        f"<var n='{esc(k)}' t='{t}'><![CDATA[{v}]]></var>"
        for k, (v, t) in variables.items()
    )
    return f"<vars>{parts}</vars>"


# ---------- handlers ----------

async def h_verchk(user, elem):
    await send(user, "<msg t='sys'><body action='apiOK' r='0'></body></msg>")


async def h_login(user, elem):
    user.name = f"Galaxy{user.id}"
    await send(
        user,
        f"<msg t='sys'><body action='logOK' r='0'>"
        f"<login id='{user.id}' mod='0' n='{esc(user.name)}'></login>"
        f"</body></msg>",
    )
    # client automatically calls getRoomList() right after login (see SysHandler.handleLoginOk)
    await h_getroomlist(user, elem)


async def h_getroomlist(user, elem):
    rooms_xml = "".join(
        f"<rm id='{r.id}' maxu='{r.max_users}' maxs='0' temp='1' game='0' "
        f"priv='0' lmb='0' ucnt='{len(r.users)}' scnt='0'>"
        f"<n><![CDATA[{esc(r.name)}]]></n>{vars_xml(r.variables)}</rm>"
        for r in rooms_by_name.values()
    )
    await send(user, f"<msg t='sys'><body action='rmList' r='0'><rmList>{rooms_xml}</rmList></body></msg>")


async def h_create_room(user, elem):
    body = elem.find("body")
    room_el = body.find("room")
    name = room_el.findtext("name") or f"room{next(next_room_id)}"
    try:
        max_users = int(room_el.findtext("max") or "12")
    except (TypeError, ValueError):
        max_users = 12

    if name in rooms_by_name:
        room = rooms_by_name[name]
    else:
        rid = next(next_room_id)
        room = Room(rid, name, max_users)
        rooms_by_name[name] = room
        rooms_by_id[rid] = room
        print(f"[room] created '{name}' (id={rid})")
        add_msg = (
            f"<msg t='sys'><body action='roomAdd' r='0'>"
            f"<rm id='{room.id}' max='{room.max_users}' spec='0' temp='1' game='0' priv='0' limbo='0'>"
            f"<name><![CDATA[{esc(name)}]]></name>{vars_xml(room.variables)}</rm>"
            f"</body></msg>"
        )
        for u in users.values():
            await send(u, add_msg)

    await do_join(user, room)


async def h_join_room(user, elem):
    body = elem.find("body")
    room_el = body.find("room")
    room_id_attr = room_el.get("id") if room_el is not None else None
    room = None
    if room_id_attr is not None:
        try:
            room = rooms_by_id.get(int(room_id_attr))
        except ValueError:
            room = None
    if room is None:
        await send(
            user,
            "<msg t='sys'><body action='joinKO' r='0'><error msg='Room not found'></error></body></msg>",
        )
        return
    await do_join(user, room)


async def do_join(user, room: Room):
    # Simulate the network latency the original (remote) SmartFox server had.
    # Without this, joining over localhost is fast enough to race ahead of
    # the client's own intro animation, causing the level to flash in early.
    if room.name != "Lobby":
        await asyncio.sleep(7)

    if user.room is not None and user.room is not room:
        await do_leave(user, notify=True)
    elif user.room is room:
        # Client re-requesting the room it's already in (this game does this
        # routinely). Just re-send joinOK, don't leave/delete/recreate.
        pass

    room.users[user.id] = user
    user.room = room
    user.player_id = len(room.users)

    userlist_xml = "".join(
        f"<u i='{u.id}' n='{esc(u.name)}' m='0' s='0' p='{u.player_id}'>{vars_xml(u.variables)}</u>"
        for u in room.users.values()
    )

    resp = (
        f"<msg t='sys'><body action='joinOK' r='{room.id}'>"
        f"<pid id='{user.player_id}'></pid>"
        f"<uLs>{userlist_xml}</uLs>"
        f"{vars_xml(room.variables)}"
        f"</body></msg>"
    )
    await send(user, resp)

    enter_msg = (
        f"<msg t='sys'><body action='uER' r='{room.id}'>"
        f"<u i='{user.id}' n='{esc(user.name)}' m='0' s='0' p='{user.player_id}'>"
        f"{vars_xml(user.variables)}</u>"
        f"</body></msg>"
    )
    await broadcast(room, enter_msg, exclude=user.id)

    ucount_msg = (
        f"<msg t='sys'><body action='uCount' r='{room.id}' u='{len(room.users)}' s='0'></body></msg>"
    )
    await broadcast(room, ucount_msg)

    print(f"[room] {user.id} joined '{room.name}' ({len(room.users)} users)")


async def do_leave(user, notify=True):
    room = user.room
    if room is None:
        return
    room.users.pop(user.id, None)
    if notify:
        leave_msg = (
            f"<msg t='sys'><body action='userGone' r='{room.id}'>"
            f"<user id='{user.id}'></user></body></msg>"
        )
        await broadcast(room, leave_msg)
    user.room = None
    print(f"[room] {user.id} left '{room.name}' ({len(room.users)} users)")
    if not room.users and room.name != "Lobby":
        rooms_by_name.pop(room.name, None)
        rooms_by_id.pop(room.id, None)
        print(f"[room] '{room.name}' deleted (empty)")


async def h_set_uvars(user, elem):
    vars_el = elem.find("body/vars")
    if vars_el is not None:
        for v in vars_el.findall("var"):
            name = v.get("n")
            t = v.get("t", "s")
            value = v.text or ""
            user.variables[name] = (value, t)

    if user.room:
        msg = (
            f"<msg t='sys'><body action='uVarsUpdate' r='{user.room.id}'>"
            f"<user id='{user.id}'></user>"
            f"{vars_xml(user.variables)}"
            f"</body></msg>"
        )
        await broadcast(user.room, msg, exclude=user.id)


async def h_set_rvars(user, elem):
    if not user.room:
        return
    vars_el = elem.find("body/vars")
    if vars_el is not None:
        for v in vars_el.findall("var"):
            name = v.get("n")
            t = v.get("t", "s")
            value = v.text or ""
            user.room.variables[name] = (value, t)

    msg = (
        f"<msg t='sys'><body action='rVarsUpdate' r='{user.room.id}'>"
        f"<user id='{user.id}'></user>"
        f"{vars_xml(user.room.variables)}"
        f"</body></msg>"
    )
    await broadcast(user.room, msg)


async def h_pubmsg(user, elem):
    if not user.room:
        return
    txt_el = elem.find("body/txt")
    txt = txt_el.text or "" if txt_el is not None else ""
    msg = (
        f"<msg t='sys'><body action='pubMsg' r='{user.room.id}'>"
        f"<user id='{user.id}'></user>"
        f"<txt><![CDATA[{txt}]]></txt>"
        f"</body></msg>"
    )
    await broadcast(user.room, msg, exclude=user.id)


async def h_leave_room(user, elem):
    await do_leave(user, notify=True)


async def h_autojoin(user, elem):
    await do_join(user, ensure_lobby())


HANDLERS = {
    "verChk": h_verchk,
    "login": h_login,
    "getRmList": h_getroomlist,
    "createRoom": h_create_room,
    "joinRoom": h_join_room,
    "setUvars": h_set_uvars,
    "setRvars": h_set_rvars,
    "pubMsg": h_pubmsg,
    "leaveRoom": h_leave_room,
    "autoJoin": h_autojoin,
}


async def dispatch(user, raw_xml: str):
    try:
        elem = ET.fromstring(raw_xml)
    except ET.ParseError as e:
        print(f"[!] parse error: {e} raw={raw_xml}")
        return
    body = elem.find("body")
    if body is None:
        return
    action = body.get("action")
    print(f"[<{user.id}] action={action}")
    fn = HANDLERS.get(action)
    if fn:
        await fn(user, elem)
    else:
        print(f"[?] unhandled action '{action}': {raw_xml}")


async def handle_client(reader, writer):
    peer = writer.get_extra_info("peername")
    uid = next(next_user_id)
    user = User(uid, writer)
    users[uid] = user
    print(f"[+] connection {peer} -> id {uid}")

    buffer = b""
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            buffer += data
            while b"\x00" in buffer:
                raw, buffer = buffer.split(b"\x00", 1)
                if not raw.strip():
                    continue
                text = raw.decode("utf-8", errors="replace")
                print(f"[{uid}] RAW: {text}")
                await dispatch(user, text)
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        print(f"[-] closed {uid}")
        await do_leave(user, notify=True)
        users.pop(uid, None)
        writer.close()


async def main():
    ensure_lobby()
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"SFS server listening on {HOST}:{PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
