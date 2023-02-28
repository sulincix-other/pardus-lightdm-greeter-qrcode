import asyncio
import qrcode

qrpopover = None
qrimage = None
qrtext = None
qrfile = os.environ["HOME"]+"/qrkod.png"
def _qrkod_button_event(widget=None):
    qrpopover.popup()
    qrkod_control_event()

qr_event_lock = False

@asynchronous
def qrkod_control_event():
    global qr_event_lock
    if qr_event_lock:
        return
    qr_event_lock = True
    lan_ip = ""
    if len(get_local_ip()) == 0:
        return
    for ip, dev in get_local_ip():
        lan_ip += "http://{}:8080\n".format(ip)
    img = qrcode.make(lan_ip.strip())
    qrtext.set_text(lan_ip.strip())
    img.save(qrfile)
    qr_event_lock = False

def update_qr_image():
    if os.path.isfile(qrfile):
        qrimage.set_from_file(qrfile)
    GLib.timeout_add(500,update_qr_image)

def module_init():
    global qrpopover
    global qrimage
    global qrtext
    if os.path.isfile(qrfile):
        os.unlink(qrfile)
    qrpopover = Gtk.Popover()
    qrimage = Gtk.Image()
    qrtext = Gtk.Label()
    b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    b.pack_start(qrimage,False,False,0)
    b.pack_start(qrtext,False,False,0)
    qrpopover.add(b)
    qrpopover.set_position(Gtk.PositionType.BOTTOM)
    button = Gtk.MenuButton(label="QR", popover=qrpopover)
    button.connect("clicked",_qrkod_button_event)
    loginwindow.o("ui_box_bottom_right").pack_end(button, False, True, 10)
    button.get_style_context().add_class("icon")
    button.show_all()
    b.show_all()
    update_qr_image()
