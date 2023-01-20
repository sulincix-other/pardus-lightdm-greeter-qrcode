import asyncio
import qrcode

qrpopover = None
qrimage = None

def _qrkod_button_event(widget=None):
    qrpopover.popup()
    GLib.idle_add(qrkod_control_event)

@asynchronous
def qrkod_control_event():
    if os.path.isfile("/tmp/qrkod.png"):
        return
    lan_ip = ""
    for ip, dev in get_local_ip():
        lan_ip += "http://{}:8080\n".format(ip)
    img = qrcode.make(lan_ip.strip())
    type(img)  # qrcode.image.pil.PilImage
    img.save("/tmp/qrkod.png")

def update_qr_image():
    if not os.path.isfile("/tmp/qrkod.png"):
        GLib.timeout_add(500,update_qr_image)
        return
    qrimage.set_from_file("/tmp/qrkod.png")

def module_init():
    global qrpopover
    global qrimage
    qrpopover = Gtk.Popover()
    qrimage = Gtk.Image()
    qrpopover.add(qrimage)
    qrpopover.set_position(Gtk.PositionType.BOTTOM)
    button = Gtk.MenuButton(label="QR", popover=qrpopover)
    button.connect("clicked",_qrkod_button_event)
    loginwindow.o("ui_box_bottom_right").pack_end(button, False, True, 10)
    button.get_style_context().add_class("icon")
    button.show_all()
    qrimage.show()
    update_qr_image()
