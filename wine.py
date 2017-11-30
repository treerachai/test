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

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

admin=[" "]
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
        sendMessage(op.param1, client.getContact(op.param1).displayName + " ขอบคุณที่รับเป็นเพื่อน\n(*´･ω･*) ")
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
        sendMessage(op.param1, client.getContact(op.param3).displayName + ", โชคดีนะ แล้วพบกันใหม่ นะ\n(*´･ω･*) ")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + ", โชคดีนะ แล้วพบกันใหม่ นะ\n(*´･ω･*) ")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return
tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def CANCEL_INVITATION_GROUP(op):
    try:
        client.cancelGroupInvitation(op.param1,[op.param3])
    except Exception as e:
        print e
        print ("\n\nCANCEL_INVITATION_GROUP\n\n")
        return

tracer.addOpInterrupt(31,CANCEL_INVITATION_GROUP)

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
                if msg.text == "กิ๊ฟ":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:

                if msg.text == "กิ๊ฟ":
                    sendMessage(msg.to, text="gift sent", contentMetadata={'prdid': 'a0768339-c2d3-4189-9653-2909e9bb6f58',
                                    'prdtype': 'theme',
                                    'msgtpl': '5'}, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "รหัส":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "รหัสกลุ่ม":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ข้อมูลกลุ่ม":
                    group = client.getGroup(msg.to)
                    md = "[ชื่อกลุ่ม]\n" + group.name + "\n\n[รหัสกลุ่ม]\n" + group.id + "\n\n[รูปภาพกลุ่ม]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nคำเชิญ URL: ที่ได้รับอนุญาต\n"
                    else: md += "\n\nคำเชิญ URL: ปฏิเสธ\n"
                    if group.invitee is None: md += "\nสมาชิก: " + str(len(group.members)) + "คน\n\nเชิญ: 0คน"
                    else: md += "\nสมาชิก: " + str(len(group.members)) + "คน\nเชิญ: " + str(len(group.invitee)) + "คน"
                    sendMessage(msg.to,md)
                if msg.text in ["คำสั่ง","Help","help"]:
                    sendMessage(msg.to,"¤ คำสั่งบอท¤\n\n¤ by treerachai ¤\n\n¤ ฉัน\n¤ รหัส\n¤ เช็คความเร็ว\n¤ กลุ่ม\n¤ รหัสกลุ่ม\n¤ ข้อมูลกลุ่ม\n¤ ขอลิ้งค์\n¤ เปิดลิ้งค์\n¤ ปิดลิ้งค์\n¤ แท็ก\n¤ นับ\n¤ อ่าน\n¤ คัดลอกข้อมูล @\n¤ สำรองข้อมูล\n¤ บล็อก @\n¤ รายการบล็อก")
                if msg.text in ["เช็คความเร็ว","Speed","speed"]:
                    start = time.time()
                    sendMessage(msg.to, text="โปรดรอสักครู่.....", contentMetadata=None, contentType=None)
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%sseconds" % (elapsed_time))										
                if "ชื่อกลุ่ม:" in msg.text:
                    key = msg.text[22:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"ชื่อกลุ่ม"+key+"เปลี่ยนไปเป็น")
                if msg.text == "ขอลิ้งค์":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "เปิดลิ้งค์":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "เปิดอยู่แล้ว")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "เปิดลิ้งค์เรียบร้อย")
                if msg.text == "ปิดลิ้งค์":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "ปิดอยู่แล้ว")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "ปิดลิ้งค์เรียบร้อย")
                if msg.text == "ยกเลิก":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "ไม่มีค้างเชิญ.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + "รายการ")
                if "เชิญ" in msg.text:
                    key = msg.text[-33:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" นั่นคือเพื่อนของฉันได้รับอนุญาตให้ป้อนข้อมูล")
                if msg.text == "ฉัน":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "แสดง" in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"'s contact")
                if msg.text == "เวลา":
                    sendMessage(msg.to, "เวลาขณะนี้ " + datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S') + " TH")
                if msg.text == "gift":
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
									
                elif msg.text in ["กลุ่ม"]:
                    gid = client.getGroupIdsJoined()
                    h = ""
                    for i in gid:
                        h += "[➣] %s\n" % (client.getGroup(i).name +"→["+str(len(client.getGroup(i).members))+"]")
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
                         print "มากกว่า 500+"
                     cnt = Message()
                     cnt.text = "Done:"+str(jml)
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
                                sendMessage(msg.to, "รายการคัคลอกข้อมูลสำเร็จ ~")
                            except Exception as e:
                                print e    
                elif msg.text in ["สำรองข้อมูล"]:
                    try:
                        client.updateDisplayPicture(backup.pictureStatus)
                        client.updateProfile(backup)
                        sendMessage(msg.to, "สำรองข้อมูลสำเร็จ")
                    except Exception as e:
                        sendMessage(msg.to, str(e))
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
                            sendMassage(msg.to, "ไม่มีข้อมูล...")
                        else:
                            for target in targets:
                                try:
                                   client.blockContact(target)
                                   sendMessage(msg.to, "บล็อกข้อมูลการติดต่อสำเร็จ~")
                                except Exception as e:
                                   print e
                elif msg.text.lower() == 'รายการบล็อก':
                    blockedlist = client.getBlockedContactIds()
                    sendMessage(msg.to, "รอสักครู่กำลังเช็คข้อมูล......")
                    kontak = client.getContacts(blockedlist)
                    num=1
                    msgs="รายการบล็อก\n"
                    for ids in kontak:
                        msgs+="\n%i. %s" % (num, ids.displayName)
                        num=(num+1)
                    msgs+="\n\nทั้งหมด %i ผู้ใช้ที่ถูกบล็อก(s)" % len(kontak)
                    sendMessage(msg.to, msgs)
                elif "ส่งข้อมูล " in msg.text:
                    cond = msg.text.split(" ")
                    target = cond[1]
                    text = msg.text.replace("Send " + str(target) + " Chat ","")
                    try:
                        client.findAndAddContactsByMid(target)
                        sendMessage(target,"From treebot : \"" + text + "\"")
                        sendMessage(msg.to,"ส่งข้อความเรียบร้อยแล้ว")
                    except:
                        sendMessage(msg.to,"ไม่สามารถส่งข้อความอยาจมีข้อมูลผิดพลาด")
												
    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
