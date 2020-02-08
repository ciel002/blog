# from manager import app


# def bootoast(message, type, position, timeout, animationDuration, dismissable):
def bootoast():
    text = "bootoast({message: " + "res.message" + "type: " + "'success'" + \
           ",position:" + "'bottom'" + ",timeout: " + "2" + ",animationDuration: " +\
           "700" + ",dismissable: " + "false" + "});"
    return text


# app.add_template_global(bootoast, 'bootoast')
