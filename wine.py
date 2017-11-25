# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json, requests, urllib

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

admin=["ucd886b532f581aa4de98af5898719392"]
wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
    }

wait2 = {    
    'copy':False,
    'target':{},
    'midsTarget':{},
    }

setTime = {}
setTime = wait["setTime"]

contact = client.getProfile() 
backup = client.getProfile() 
backup.dispalyName = contact.displayName 
backup.statusMessage = contact.statusMessage
backup.pictureStatus = contact.pictureStatus

wait2 = {    
    'message':"Thanks for add me" 
    }

def mention(to,nama):
    aa = ""
    bb = ""
    strt = int(0)
    akh = int(0)
    nm = nama
    print nm
    for mm in nama:
      akh = akh + 3
      aa += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(mm)+"},"""
      strt = strt + 4
      akh = akh + 1
      bb += "@x \n"
    aa = (aa[:int(len(aa)-1)])
    msg = Message()
    msg.to = to
    msg.from_ = profile.mid
    msg.text = bb
    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+aa+']}','EMTVER':'4'}
    print msg
    try:
       client.sendMessage(msg)
    except Exception as error:
        print error
 
def post_content(self, urls, data=None, files=None):
        return self._session.post(urls, headers=self._headers, data=data, files=files)

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)
    
def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + " ขอบคุณที่รับเป็นเพื่อน\n(*´･ω･*)")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + ", ยินดีต้อนรับ\n(*´･ω･*) ")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
#				client.kickoutFromGroup(op.param1,[op.param2])
#				client.inviteIntoGroup(op.param1,[op.param3])
				sendMessage(op.param1, client.getContact(op.param2).displayName + ", โชคดีนะ แล้วพบกันใหม่ นะ\n(*´･ω･*) ")				
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_UPDATE_GROUP(op):
    try:
                sendMessage(op.param1, client.getContact(op.param2).displayName + ", โชคดีนะ แล้วพบกันใหม่ นะ\n(*´･ω･*) ")
#                client.kickoutFromGroup(op.param1,[op.param2])
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_UPDATE_GROUP\n\n")
        return

tracer.addOpInterrupt(11,NOTIFIED_UPDATE_GROUP)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                elif wait["ติดต่อ"] == True:
                    msg.contentType = 0
                    sendMessage(msg.to,msg.contentMetadata["mid"])
                    if 'displayName' in msg.contentMetadata:
                        contact = client.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = client.channel.getCover(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        sendMessage(msg.to,"[displayName]:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                    else:
                        contact = client.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = client.channel.getCover(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        sendMessage(msg.to,"[displayName]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                if msg.text == "กิ๊ฟ":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text in ["คำสั่ง","Help","help"]:
                    sendMessage(msg.to,"¤ คำสั่งเซลบอท¤\n\n¤ me\n¤ mid \n¤ เช็คความเร็ว\n¤ กลุ่ม\n¤ gid\n¤ ginfo\n¤ ลิ้ง\n¤ เปิดลิ้ง\n¤ ปิดลิ้ง\n¤ แท็ก\n¤ นับ 「เริ่มเช็คคนอ่าน」\n¤ อ่าน 「อ่านคนแอบ」\n¤ คัดลอกข้อมูล @\n¤ สำรองข้อมูล\n¤ บล็อก @\n¤ รายการบล็อก")
                if msg.text in ["เช็คความเร็ว","Speed","speed"]:
                    start = time.time()
                    sendMessage(msg.to, text="ตรวจสอบข้อมูลสักครู่...", contentMetadata=None, contentType=None)
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%sseconds" % (elapsed_time))
                elif msg.text in ["กลุ่ม"]:
                    gid = client.getGroupIdsJoined()
                    h = ""
                    for i in gid:
                        h += "[★] %s\n" % (client.getGroup(i).name +"→["+str(len(client.getGroup(i).members))+"]")
                    sendMessage(msg.to,"[รายชื่อกลุ่ม]\n"+ h +"กลุ่มทั้งหมด =" +"["+str(len(gid))+"]")
                if msg.text in["แท็ก"]:
                     group = client.getGroup(msg.to)
                     nama = [contact.mid for contact in group.members]
                     nm1, nm2, nm3, nm4, nm5, nm6, jml = [], [], [], [], [], [], len(nama)
                     if jml <= 100:
                        mention(msg.to, nama)
                     if jml > 100 and jml < 200:
                        for i in range(0, 99):
                            nm1 += [nama[i]]
                        mention(msg.to, nm1)
                        for j in range(100, len(nama)-1):
                            nm2 += [nama[j]]
                        mention(msg.to, nm2)
                     if jml > 200  and jml < 500:
                        for i in range(0, 99):
                            nm1 += [nama[i]]
                        mention(msg.to, nm1)
                        for j in range(100, 199):
                            nm2 += [nama[j]]
                        mention(msg.to, nm2)
                        for k in range(200, 299):
                            nm3 += [nama[k]]
                        mention(msg.to, nm3)
                        for l in range(300, 399):
                            nm4 += [nama[l]]
                        mention(msg.to, nm4)
                        for m in range(400, 499):
                            nm5 += [nama[m]]
                        mention(msg.to, nm5)
                        for n in range(500, len(nama)-1):
                            nm6 += [nama[n]]
                        mention(msg.to, nm6)
                     if jml > 500:
                         print "มากกว่า 500+"
                     cnt = Message()
                     cnt.text = "เสร็จแล้ว:"+str(jml)
                     cont.to = msg.to
                     client.sendMessage(cnt)
                     
                elif "คัดลอกข้อมูล @" in msg.text:
                    print "[Copy] OK"
                    _name = msg.text.replace("คัดลอกข้อมูล @","")
                    _nametarget = _name.rstrip(' ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        sendMassage(msg.to, "ไม่มีข้อมูล...")
                    else:
                        for target in targets:
                            try:
                                client.CloneContactProfile(target)
                                sendMessage(msg.to, "คัคลอกข้อมูลสำเร็จ ~ ")
                            except Exception as e:
                                print e
    
                elif msg.text in ["สำรองข้อมูล","backup"]:
                    try:
                        client.updateDisplayPicture(backup.pictureStatus)
                        client.updateProfile(backup)
                        sendMessage(msg.to, "สำรองข้อมูลสำเร็จ ~ ")
                    except Exception as e:
                        sendMessage(msg.to, str(e))
                elif msg.text.lower() == 'รายการบล็อก':
                    blockedlist = client.getBlockedContactIds()
                    sendMessage(msg.to, "ตรวจสอบข้อมูลสักครู่...")
                    kontak = client.getContacts(blockedlist)
                    num=1
                    msgs="รากการบล็อกที่มี\n"
                    for ids in kontak:
                        msgs+="\n%i. %s" % (num, ids.displayName)
                        num=(num+1)
                    msgs+="\n\nทั้งหมด %i รายการที่บล็อก(s)" % len(kontak)

                elif "ส่งข้อความ " in msg.text:
                    cond = msg.text.split(" ")
                    target = cond[1]
                    text = msg.text.replace("Send " + str(target) + " Chat ","")
                    try:
                        client.findAndAddContactsByMid(target)
                        sendMessage(target,"จาก TREEBOT : \"" + text + "\"")
                        sendMessage(msg.to,"ส่งข้อความเรียบร้อยแล้ว")
                    except:
                        sendMessage(msg.to,"ไม่สามารถส่งข้อความอาจมีข้อมูลผิดพลาด")
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Error"
                    md = "[ชื่อกลุ่ม : ]\n" + group.name + "\n\n[รหัสกลุ่ม : ]\n" + group.id + "\n\n[ผู้สร้างกลุ่ม :]\n" + gCreator + "\n\n[ภาพกลุ่ม : ]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nรหัส Url : ได้รับอนุญาต"
                    else: md += "\n\nรหัส Url : ถูกปิดกั้น"
                    if group.invitee is None: md += "\nจำนวนสมาชิก : " + str(len(group.members)) + " คน" + "\nคำเชิญที่ยังไม่ได้ตอบ : 0 คน"
                    else: md += "\nจำนวนสมาชิก : " + str(len(group.members)) + " คน" + "\nคำเชิญที่ยังไม่ได้ตอบ : " + str(len(group.invitee)) + " คน"
                    sendMessage(msg.to,md)
                elif "บล็อก @" in msg.text:
                    if msg.toType == 2:
                        print "[bloc] OK"
                        _name = msg.text.replace("บล็อก @","")
                        _nametarget = _name.rstrip('  ')
                        gs = client.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _nametarget == g.displayName:
                               targets.append(g.mid)
                        if targets == []:
                            sendMassage(msg.to, "ไม่พบข้อมูล......")
                        else:
                            for target in targets:
                                try:
                                   client.blockContact(target)
                                   sendMessage(msg.to, "บล็อกการติดต่อสำเร็จ~")
                                except Exception as e:
                                   print e
                elif msg.text.lower() == 'รายกการบล็อก':
                    blockedlist = client.getBlockedContactIds()
                    sendMessage(msg.to, "ตรวจอบข้อมูลสักครู่...")
                    kontak = client.getContacts(blockedlist)
                    num=1
                    msgs="รายการบล็อกที่มี\n"
                    for ids in kontak:
                        msgs+="\n%i. %s" % (num, ids.displayName)
                        num=(num+1)
                    msgs+="\n\nทั้งหมดl %i รายการที่บล็อก(s)" % len(kontak)
                    sendMessage(msg.to, msgs)
                elif msg.text.lower() == 'gid':
                    gid = client.getGroupIdsJoined()
                    h = ""
                    for i in gid:
                        h += " %s\nID : %s\n" % (client.getGroup(i).name,i)
                    sendMessage(msg.to,h)
                elif msg.text.lower() == 'เลิกกัน':
                    gid = client.getGroupIdsJoined()
                    for i in gid:
                        client.leaveGroup(i)
                    if wait["lang"] == "JP":
                        sendMessage(msg.to,"ออกจากทุกกลุ่ม")
                    else:
                        sendMessage(msg.to,"เขาปฏิเสธคำเชิญทั้งหมด")
                elif "ชีวภาพ " in msg.text:
                    string = msg.text.replace("ชีวภาพ ","")
                    if len(string.decode('utf-8')) <= 60000000000:
                        profile = client.getProfile()
                        profile.statusMessage = string
                        client.updateProfile(profile)
                        sendMessage(msg.to,"􀜁􀇔􏿿Update Bio👉" + string + "👈")
                elif "ชื่อ " in msg.text:
                    string = msg.text.replace("ชื่อ ","")
                    if len(string.decode('utf-8')) <= 60000000:
                        profile = client.getProfile()
                        profile.displayName = string
                        client.updateProfile(profile)
                        sendMessage(msg.to,"􀜁􀇔􏿿อัปเดตชื่อ👉 " + string + "👈")
                elif "ขโมย @" in msg.text:          
                   _name = msg.text.replace("ขโมย @","")
                   _nametarget = _name.rstrip('  ')
                   gs = client.getGroup(msg.to)
                   targets = []
                   for g in gs.members:
                       if _nametarget == g.displayName:
                           targets.append(g.mid)
                   if targets == []:
                       sendMessage(msg.to,"Contact not found")
                   else:
                       for target in targets:
                           try:
                               contact = client.getContact(target)
                               path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                               client.sendImageWithURL(msg.to, path)
                           except:
                               pass
                elif "เรียบ" in msg.text:
                       nk0 = msg.text.replace("เรียบ","")
                       nk1 = nk0.lstrip()
                       nk2 = nk1.replace("all","")
                       nk3 = nk2.rstrip()
                       _name = nk3
                       gs = client.getGroup(msg.to)
                       targets = []
                       for g in gs.members:
                           if _name in g.displayName:
                              targets.append(g.mid)
                       if targets == []:
                           sendMassage(msg.to,"ไม่มีสมาชิก")
                           pass
                       else:
                           for target in targets:
                              try:
                                  client.kickoutFromGroup(msg.to,[target])
                                  print (msg.to,[g.mid])
                              except:
                                  sendMessage(msg.to,"Rata? Protect Anjeng")
                                  sendMessage(msg.to,"masih mauko sundala")

                elif "mid @" in msg.text:
                    _name = msg.text.replace("Mid @","")
                    _nametarget = _name.rstrip(' ')
                    gs = client.getGroup(msg.to)
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            sendMessage(msg.to, g.mid)
                        else:
                            pass
                elif "เชิญ " in msg.text:
                    midd = msg.text.replace("เชิญ ","")
                    client.findAndAddContactsByMid(midd)
                    client.inviteIntoGroup(msg.to,[midd])
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if "gn" in msg.text:
                    key = msg.text[22:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"ชื่อกลุ่ม"+key+"เปลี่ยนเป็น")
                if msg.text == "ลิ้ง":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if "ร่วม" in msg.text:
                    G = client.getGroup(msg.to)
                    ginfo = client.getGroup(msg.to)
                    G.preventJoinByTicket = False
                    client.updateGroup(G)
                    invsend = 0
                    Ticket = client.reissueGroupTicket(msg.to)
                    client.acceptGroupInvitationByTicket(msg.to,Ticket)
                if msg.text == "เปิดลิ้ง":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "ลิ้งค์เปิดอยู่")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "เปิดลิ้งค์เรียบร้อย")
                if msg.text == "ปิดลิ้ง":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "ลิ้งค์ปิดอยู่")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "ปิดลิ้งค์เรียบร้อย")
                if msg.text == "ยกเลิก":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "ไม่มีสมาชิกค้างเชิญ.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + "ยกเลิกเชิญเรียบร้อย")
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "โชว์ " in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"'s contact")
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "เวลา":
                    sendMessage(msg.to, "today " + datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S') + " WIB")
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "นับ":
                    sendMessage(msg.to, "รอสักครู่กำลังเช็ค")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "อ่าน":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "รายชื่อที่ตรวจพบทั้งหมด %s\n\nชื่อที่มีทั้งหมด\n%sตรวจพบ\n\nวัน & เวลา:\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "เช็คการตั้งค่าการอ่าน")
																			 
    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
