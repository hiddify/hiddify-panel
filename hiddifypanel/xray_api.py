import xtlsapi

def get_xray_client():
    return XrayClient('127.0.0.1', 10085)
    
def get_inbound_tags():
    xray_client=get_xray_client()
    return [inb.name.split(">>>")[1] for inb in xray_client.stats_query('inbound')]

def add_client(uuid,tags):
    xray_client=get_xray_client()
    tags=xray_api.get_inbound_tags()
    for t in tags:
        try:
            alter_id=0 if 'vmess' in t else None
            xray_client.add_client(t,f'{uuid}', f'{uuid}@hiddify.com',alter_id=alter_id)
        except Exception as e:
            print(f"error in add  {uuid} {tag} {e}" )
            pass

def remove_client(uuid):
    xray_client=get_xray_client()
    tags=xray_api.get_inbound_tags()
    for t in tags:
        try:
            xray_client.remove_client(t, f'{uuid}@hiddify.com')
        except Exception as e:
            print(f"error in remove  {uuid} {tag} {e}" )
            pass        

def get_usage(uuid,reset=False):
    d = xray_client.get_client_download_traffic(f'{uuid}@hiddify.com',reset=reset)
    u = xray_client.get_client_upload_traffic(f'{uuid}@hiddify.com',reset=reset)
    if d is None or u is None:
        return None
    return d+u