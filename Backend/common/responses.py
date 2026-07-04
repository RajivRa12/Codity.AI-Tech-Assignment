def success_response(data=None, message='OK'):
    return {'status':'success','message':message,'data':data}

def error_response(message='Error', code=None, details=None):
    return {'status':'error','message':message,'code':code,'details':details}
