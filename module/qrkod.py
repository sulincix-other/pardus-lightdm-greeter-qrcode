import asyncio
import qrcode

qrpopover = None
qrlabel = None
qrimage = None

def _qrkod_button_event(widget=None):
    qrlabel.set_text(_("Loading..."))
    qrpopover.popup()
    qrkod_control_event()
    #GLib.idle_add(qrkod_control_event)
	
@asynchronous
def qrkod_control_event():
    lan_ip = ""
    # Calculate line length
    i = 0
    for ip, dev in get_local_ip():
        j = len(ip) + len(dev) + 3
        if j > i:
            i = j
    for ip, dev in get_local_ip():
        j = len(ip) + len(dev) + 2
        lan_ip += "https:{}:8080\n".format(ip)
    ctx = _("{}").format(lan_ip)

    img = qrcode.make(ctx.strip())
    type(img)  # qrcode.image.pil.PilImage
    img.save("/tmp/qrkod.png")
    qrimage.set_from_file("/tmp/qrkod.png")
    qrlabel.set_text("Qr Kod Giriş")


def module_init():
    global qrpopover
    global qrlabel
    global qrimage
    qrpopover = Gtk.Popover()
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    qrlabel = Gtk.Label()
    qrimage = Gtk.Image()
    qrpopover.add(vbox)
    qrpopover.set_position(Gtk.PositionType.BOTTOM)
    button = Gtk.MenuButton(label="QR", popover=qrpopover)
    button.connect("clicked",_qrkod_button_event)
    vbox.pack_start(qrlabel, False, True, 10)
    vbox.pack_start(qrimage, False, True, 10)
    loginwindow.o("ui_box_bottom_right").pack_start(button, False, True, 10)
    button.show_all()
    vbox.show_all()
