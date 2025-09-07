from flask import flash

def flash_success(msg):
    flash(msg, "success")

def flash_error(msg):
    flash(msg, "danger")

