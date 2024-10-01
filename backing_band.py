import tulip, midi, music, random, time
import lvgl as lv

def note(t):
    global app
    app.synth.note_on(random.choice(app.chord), 0.6, time=t)

def play(event):
    global app
    if app.slot == None:
        app.slot = tulip.seq_add_callback(note, 24)

def pause(event):
    global app
    if app.slot != None:
        tulip.seq_remove_callback(app.slot)
        app.slot = None

def start(app):
    pass
    
def stop(app):
    pause(None)
    app.synth.release()

def bpm_change(event):
    global app
    tulip.seq_bpm(event.get_target_obj().get_value()*1.5)
    app.bpm_label.label.set_text(str(tulip.seq_bpm()))

def bpm_dec(event):
    bpm_alter(-1)

def bpm_inc(event):
    bpm_alter(1)

def bpm_alter(delta):
    global app
    tulip.seq_bpm(tulip.seq_bpm()+delta)
    app.bpm_label.label.set_text(current_int_bpm())
    time.sleep(0.1)

def current_int_bpm():
    int_val = int(tulip.seq_bpm())
    str_val = str(int_val)
    if int_val < 100:
        str_val = ' '+str_val
    return str_val

def run(screen):
    global app
    app = screen
    tulip.UIScreen.load_delay = 10
    tulip.UIScreen.default_offset_x = 10
    tulip.UIScreen.default_offset_y = 10
    app.slot = None
    tulip.seq_bpm(100)
    app.chord = music.Chord("F:min7").midinotes()
    app.synth = midi.Synth(num_voices=1, patch_number=143)  # DX7 BASS 2
    dec_pbm_button = tulip.UIButton(lv.SYMBOL.DOWN, font=lv.font_montserrat_18)
    dec_pbm_button.button.add_event_cb(bpm_dec, lv.EVENT.PRESSING, None)
    inc_pbm_button = tulip.UIButton(lv.SYMBOL.UP, font=lv.font_montserrat_18)
    inc_pbm_button.button.add_event_cb(bpm_inc, lv.EVENT.PRESSING, None)
    app.bpm_label = tulip.UILabel(current_int_bpm(), font=lv.font_unscii_16)
    app.bpm_label.label.set_style_text_align(lv.TEXT_ALIGN.CENTER,0)
    app.bpm_label.label.set_style_bg_color(lv.color_hex(0x003a57), lv.PART.MAIN)
    app.add(tulip.UILabel('BPM', font=lv.font_montserrat_24), x=10, y=20)
    app.add(dec_pbm_button, x=70, y=-10)
    app.add(app.bpm_label, x=160, y=25)
    app.add(inc_pbm_button, x=210, y=-10) 
    play_button = tulip.UIButton(lv.SYMBOL.PLAY, font=lv.font_montserrat_18, callback=play)
    pause_button = tulip.UIButton(lv.SYMBOL.PAUSE, font=lv.font_montserrat_18, callback=pause)
    app.add(play_button, x=340, y=-10)
    app.add(pause_button, x=420, y=-10)
    # replace the default quit and tab buttons
    screen.alttab_button = tulip.UIButton(lv.SYMBOL.SHUFFLE, font=lv.font_montserrat_18, callback=screen.alttab_callback)
    app.add(screen.alttab_button, x=870, y=-10)
    screen.quit_button = tulip.UIButton(lv.SYMBOL.CLOSE, font=lv.font_montserrat_18, callback=screen.screen_quit_callback)
    app.quit_button.button.set_style_bg_color(tulip.pal_to_lv(128), lv.PART.MAIN)
    app.add(screen.quit_button, x=950, y=-10)
    
    # bpm_slider = tulip.UISlider(tulip.seq_bpm()/1.5, w=600, h=25,
    #     callback=bpm_change, bar_color=123, handle_color=23)
    # app.add(bpm_slider, x=150,y=100)
    app.present()
    app.quit_callback = stop
    start(app)