# -*- coding: utf-8 -*-
from wine import LineClient
from wine.LineApi import LineTracer
from wine.LineThrift.ttypes import Message
from wine.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json, requests, urllib

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")
#client._tokenLogin("EmtSwQkN3TjWRrT0wfa7.0LutO9fOymTF5KfIofqfDW.plBPA8v7fYD8hrTK09tzX+GoIgx5oByaZlHvEu9/9V0=")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

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
    'message':"Thanks for add me," 
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
        sendMessage(op.param1, client.getContact(op.param1).displayName + " ขอบคุณที่รับเป็นเพื่อน\n (*´･ω･*)")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + ", , ยินดีต้อนรับ\n (*´･ω･*)")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
#				client.kickoutFromGroup(op.param1,[op.param2])
#				client.inviteIntoGroup(op.param1,[op.param3])
				sendMessage(op.param1, client.getContact(op.param2).displayName + ", โชคดีนะ แล้วพบกันใหม่ นะ\n (*´･ω･*)")				
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_UPDATE_GROUP(op):
    try:
                sendMessage(op.param1, client.getContact(op.param2).displayName + ", โชคดีนะ แล้วพบกันใหม่ นะ\n (*´･ω･*) ")
#                client.kickoutFromGroup(op.param1,[op.param2])
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_UPDATE_GROUP\n\n")
        return

tracer.addOpInterrupt(11,NOTIFIED_UPDATE_GROUP)

def NOTIFIED_CANCEL_INVITATION_GROUP(op):
    try:
                sendMessage(op.param1, client.getContact(op.param2).displayName + ", โชคดีนะ แล้วพบกันใหม่ นะ\n (*´･ω･*) ")
#                client.kickoutFromGroup(op.param1,[op.param2])
#                client.inviteIntoGroup(op.param1,[op.param3])
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_CANCEL_INVITATION_GROUP\n\n")
        return

tracer.addOpInterrupt(32,NOTIFIED_CANCEL_INVITATION_GROUP)

#def CANCEL_INVITATION_GROUP(op):
#    try:
#        client.cancelGroupInvitation(op.param1,[op.param3])
#    except Exception as e:
#        print e
#        print ("\n\nCANCEL_INVITATION_GROUP\n\n")
#        return
#
#tracer.addOpInterrupt(31,CANCEL_INVITATION_GROUP)

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
                if msg.text == "รหัส":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ฉัน":
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
                        sendMessage(msg.to,"[ชื่อที่แสดง]:\n" + msg.contentMetadata["displayName"] + "\n[รหัส]:\n" + msg.contentMetadata["mid"] + "\n[สถานะข้อความ]:\n" + contact.statusMessage + "\n[รูปภาพสถานะ]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[ปก URL]:\n" + str(cu))
                    else:
                        contact = client.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = client.channel.getCover(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        sendMessage(msg.to,"[ชื่อที่แสดง]:\n" + contact.displayName + "\n[รหัส]:\n" + msg.contentMetadata["mid"] + "\n[สถานะข้อความ]:\n" + contact.statusMessage + "\n[รูปภาพสถานะs]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                if msg.text == "กิ๊ฟ":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text in ["คำสั่ง","Help","help"]:
                    sendMessage(msg.to,"¤ คำสั่งกลุ่ม ¤\n\n¤ ฉัน\n¤ รหัส\n¤ เช็คความเร็ว\n¤ กลุ่ม\n¤ รหัสกลุ่ม\n¤ ข้อมูลกลุ่ม\n¤ ลิ้งค์กลุ่ม\n¤ ขอลิ้งค์\n¤ เปิดลิ้งค์\n¤ ปิดลิ้งค์\n¤ แท็ก\n¤ นับ\n¤ อ่าน\n¤ ขโมย @\n¤ คัดลอกข้อมูล @\n¤ สำรองข้อมูล\n¤ บล็อก @\n¤ รายการบล็อก\n¤ เตะ @")
                if msg.text in ["เช็คความเร็ว","Speed","speed"]:
                    start = time.time()
                    sendMessage(msg.to, text="โปรดรอสักครู่...", contentMetadata=None, contentType=None)
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%sseconds" % (elapsed_time))
                elif msg.text in ["กลุ่ม"]:
                    gid = client.getGroupIdsJoined()
                    h = ""
                    for i in gid:
                        h += "[¤] %s\n" % (client.getGroup(i).name +"→["+str(len(client.getGroup(i).members))+"]")
                    sendMessage(msg.to,"[รายชื่อกลุ่ม]\n"+ h +"กลุ่มรวม =" +"["+str(len(gid))+"]")
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
                         print "มากเกิน 500+"
                     cnt = Message()
                     cnt.text = "เรียบร้อย:"+str(jml)
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
                                sendMessage(msg.to, "รายการคัดลอกข้อมูลสำเร็จ ~")
                            except Exception as e:
                                print e
    
                elif msg.text in ["สำรองข้อมูล"]:
                    try:
                        client.updateDisplayPicture(backup.pictureStatus)
                        client.updateProfile(backup)
                        sendMessage(msg.to, "รายการสำรองข้อมูลสำเร็จ")
                    except Exception as e:
                        sendMessage(msg.to, str(e))
                elif "สแปม @" in msg.text:
                    _name = msg.text.replace("สแปม @","")
                    _nametarget = _name.rstrip(' ')
                    gs = client.getGroup(msg.to)
                    for g in gs.members:
                        if _nametarget == g.displayName:
                           sendMessage(g.mid,"สแปม !") 
                           sendMessage(g.mid,"สแปม !")
                           sendMessage(g.mid,"ขอบคุณที่ได้เห็นแล้ว")
                           sendMessage(g.mid,"ขอโทษ")
                           print " สแปม !"
                elif "ส่งข้อความ " in msg.text:
                    cond = msg.text.split(" ")
                    target = cond[1]
                    text = msg.text.replace("ส่งข้อความ " + str(target) + " พูดคุย ","")
                    try:
                        client.findAndAddContactsByMid(target)
                        sendMessage(target,"จาก TreeBot : \"" + text + "\"")
                        sendMessage(msg.to,"ส่งข้อความเรียบร้อยแล้ว")
                    except:
                        sendMessage(msg.to,"ไม่สามารถส่งข้อความอาจมีข้อมูลผิดพลาด")
                if msg.text == "ข้อมูลกลุ่ม":
                    group = client.getGroup(msg.to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Error"
                    md = "[ชื่อกลุ่ม : ]\n" + group.name + "\n\n[รหัสกลุ่ม : ]\n" + group.id + "\n\n[ผู้สร้างกลุ่ม :]\n" + gCreator + "\n\n[ภาพกลุ่ม : ]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nรหัส URL : ได้รับอนุญาต"
                    else: md += "\n\nรหัส URL : ถูกปิดกั้น"
                    if group.invitee is None: md += "\nจำนวนสมาชิก : " + str(len(group.members)) + " คน" + "\nคำเชิญที่ยังไม่ได้ตอบ : 0 คน"
                    else: md += "\nจำนวนสมาชิก : " + str(len(group.members)) + " คน" + "\nคำเชิญที่ยังไม่ได้ตอบ : " + str(len(group.invitee)) + " คน"
                    sendMessage(msg.to,md)
                elif "บล็อก @" in msg.text:
                    if msg.toType == 2:
                        print "[block] OK"
                        _name = msg.text.replace("บล็อก @","")
                        _nametarget = _name.rstrip('  ')
                        gs = client.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _nametarget == g.displayName:
                               targets.append(g.mid)
                        if targets == []:
                            sendMassage(msg.to, "ไม่พบข้อมูล...")
                        else:
                            for target in targets:
                                try:
                                   client.blockContact(target)
                                   sendMessage(msg.to, "บล็อกการติดต่อสำเร็จ ~ ")
                                except Exception as e:
                                   print e
                elif msg.text.lower() == 'รายการบล็อก':
                    blockedlist = client.getBlockedContactIds()
                    sendMessage(msg.to, "โปรดรอสกครู่...")
                    kontak = client.getContacts(blockedlist)
                    num=1
                    msgs="รายชื่อผู้ใช้ที่ถูกบล็อก\n"
                    for ids in kontak:
                        msgs+="\n%i. %s" % (num, ids.displayName)
                        num=(num+1)
                    msgs+="\n\nทั้งหมด %i ผู้ใช้ที่ถูกบล็อก(s)" % len(kontak)
                    sendMessage(msg.to, msgs)
                elif msg.text.lower() == 'รหัสกลุ่ม':
                    gid = client.getGroupIdsJoined()
                    h = ""
                    for i in gid:
                        h += " %s\nรหัส : %s\n" % (client.getGroup(i).name,i)
                    sendMessage(msg.to,h)
                elif msg.text.lower() == 'ปลด':
                    gid = client.getGroupIdsJoined()
                    for i in gid:
                        client.leaveGroup(i)
                    if wait["lang"] == "JP":
                        sendMessage(msg.to,"ปลดแล้วในทุกกลุ่ม")
                    else:
                        sendMessage(msg.to,"เขาปฏิเสธคำเชิญทั้งหมด")
                elif "ชีวภาพ " in msg.text:
                    string = msg.text.replace("ชีวภาพ ","")
                    if len(string.decode('utf-8')) <= 60000000000:
                        profile = client.getProfile()
                        profile.statusMessage = string
                        client.updateProfile(profile)
                        sendMessage(msg.to,"อัพเดทชีวภาพ👉" + string + "👈")
                elif "ชื่อ" in msg.text:
                    string = msg.text.replace("ชื่อ","")
                    if len(string.decode('utf-8')) <= 60000000:
                        profile = client.getProfile()
                        profile.displayName = string
                        client.updateProfile(profile)
                        sendMessage(msg.to,"อัพเดทชื่อ👉 " + string + "👈")
                elif "ขโมย @" in msg.text:          
                   _name = msg.text.replace("ขโมย @","")
                   _nametarget = _name.rstrip('  ')
                   gs = client.getGroup(msg.to)
                   targets = []
                   for g in gs.members:
                       if _nametarget == g.displayName:
                           targets.append(g.mid)
                   if targets == []:
                       sendMessage(msg.to,"ไม่พบข้อมูลติดต่อ")
                   else:
                       for target in targets:
                           try:
                               contact = client.getContact(target)
                               path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                               client.sendImageWithURL(msg.to, path)
                           except:
                               pass
                elif msg.text in ["ลิ้งกลุ่ม"]:
                    if msg.toType == 2:
                        x = client.getGroup(msg.to)
                        if x.preventJoinByTicket == True:
                            x.preventJoinByTicket = False
                            client.updateGroup(x)
                        gurl = client.reissueGroupTicket(msg.to)
                        sendMessage(msg.to,"line://ti/g/" + gurl)
                    else:
                        if wait["lang"] == "JP":
                            sendMessage(msg.to,"ไม่สามารถใช้นอกกลุ่มได้")
                        else:
                            sendMessage(msg.to,"ไม่ใช้งานน้อยกว่ากลุ่ม")
                elif "รหัส @" in msg.text:
                    _name = msg.text.replace("รหัส @","")
                    _nametarget = _name.rstrip(' ')
                    gs = client.getGroup(msg.to)
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            sendMessage(msg.to, g.mid)
                        else:
                            pass
                elif "เตะ " in msg.text:
                    nk0 = msg.text.replace("เตะ ","")
                    nk1 = nk0.lstrip()
                    nk2 = nk1.replace("@","")
                    nk3 = nk2.rstrip()
                    _name = nk3
                    gs = client.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        sendMessage(msg.to,"ไม่พบผู้ใช้")
                        pass
                    else:
                        for target in targets:
                            try:
                                client.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                print(msg.to,"ถอดตัวออก")
                                print(msg.to,"ถอดตัวออก!!!")
                elif "เชิญ " in msg.text:
                    midd = msg.text.replace("เชิญ ","")
                    client.findAndAddContactsByMid(midd)
                    client.inviteIntoGroup(msg.to,[midd])
                elif "เตะ " in msg.text:
                    midd = msg.text.replace("เตะ ","")
                    client.kickoutFromGroup(msg.to,[midd])
                elif ("เตะ " in msg.text):
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                       try:
                          client.kickoutFromGroup(msg.to,[target])
                       except:
                          pass
                elif "แผ่" in msg.text:
                  if msg.from_ in admin:
                       nk0 = msg.text.replace("แผ่","")
                       nk1 = nk0.lstrip()
                       nk2 = nk1.replace("ทั้งหมด","")
                       nk3 = nk2.rstrip()
                       _name = nk3
                       gs = client.getGroup(msg.to)
                       targets = []
                       for s in gs.members:
                           if _name in s.displayName:
                              targets.append(s.mid)
                       if targets == []:
                           sendMessage(msg.to,"กลุ่มที่ขาดหายไป")
                           pass
                       else:
                           for target in targets:
                                try:
                                    klist=[client]
                                    kicker=random.choice(klist)
                                    kicker.kickoutFromGroup(msg.to,[target])
                                    print (msg.to,[g.mid])
                                except:
                                    sendMessage(msg.to,"ออก โดยการ เตะ....")
                                    sendMessage(msg.to,"Hehehe")
                elif "bc:ct " in msg.text:
                    bctxt = msg.text.replace("bc:ct ", "")
                    a = client.getAllContactIds()
                    for manusia in a:
                        sendMessage(manusia, (bctxt))
                elif "bc:group " in msg.text:
                    bctxt = msg.text.replace("bc:group ", "")
                    n = client.getGroupIdsJoined()
                    for manusia in n:
                        sendMessage(manusia, (bctxt))
                elif "สแปม " in msg.text:
                   txt = msg.text.split(" ")
                   jmlh = int(txt[2])
                   teks = msg.text.replace("สแปม "+str(txt[1])+" "+str(jmlh)+ " ","")
                   tulisan = jmlh * (teks+"\n")
                   if txt[1] == "on":
                        if jmlh <= 100000:
                             for x in range(jmlh):
                                    sendMessage(msg.to, teks)
                        else:
                               sendMessage(msg.to, "เกินขีด จำกัด !!! ")
                   elif txt[1] == "off":
                         if jmlh <= 100000:
                               sendMessage(msg.to, tulisan)
                         else:
                               sendMessage(msg.to, "เกินขีด จำกัด !!!! ")
                if msg.text == "isyl":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "isyld]6j,":
                    sendMessage(msg.to, msg.to)
                if "ชื่อกลุ่ม" in msg.text:
                    key = msg.text[22:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"ชื่อกลุ่ม"+key+"เปลี่ยนเป็น")
                if msg.text == "ขอลิ้งค์":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if "เข้าร่วม" in msg.text:
                    G = client.getGroup(msg.to)
                    ginfo = client.getGroup(msg.to)
                    G.preventJoinByTicket = False
                    client.updateGroup(G)
                    invsend = 0
                    Ticket = client.reissueGroupTicket(msg.to)
                    client.acceptGroupInvitationByTicket(msg.to,Ticket)
                if msg.text == "เปิดลิ้งค์":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "เปิดลิ้งค์อยู่แล้ว")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "เปิดลิ้งค์เรียบร้อย")
                if msg.text == "ปิดลิ้งค์":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "ปิดลิ้งค์อยู่แล้ว")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "ปิดลิ้งค์เรียบร้อย")
                if msg.text == "ยกเลิก":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "ไม่มีคัางเชิญ.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " ยกเลิกเรียบร้อย")
                if msg.text == "ฉัน":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "แสดง " in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"'s contact")
                if msg.text == "กิ๊ฟ":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "นับ":
                    sendMessage(msg.to, "รอสักครู่กำลังเช็คข้อมูล")
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
                else:
                    pass
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
