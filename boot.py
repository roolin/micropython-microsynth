import network, esp, machine

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
ap = network.WLAN(network.AP_IF)
ap.active(False)

esp.osdebug(None)
machine.freq(240000000)

