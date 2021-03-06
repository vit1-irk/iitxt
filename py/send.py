import ii, urllib.request, base64, codecs, os

def outcount():
    if not os.path.exists("../base/out/.outcount"):
        codecs.open("../base/out/.outcount", "w", "utf-8").write("0")
    i = str(int(codecs.open("../base/out/.outcount", "r", "utf-8").read()) + 1)
    codecs.open("../base/out/.outcount", "w", "utf-8").write(i)
    return "../base/out/%s.out" % i.zfill(5)

def find_new():
    for echo in ii.echoes:
        lst = [x for x in os.listdir("../mail/" + echo) if "new" in x]
        for msg_file in lst:
            new = codecs.open("../mail/%s/%s" % (echo, msg_file), "r", "utf-8").read().split("\n")
            header = new.index("")
            if header == 2:
                buf = [echo] + new
            elif header == 3:
                buf = [echo] + new[1:4] + ["@repto:%s" % new[0]] + new[4:]
            codecs.open(outcount(), "w", "utf-8").write("\n".join(buf))
            os.remove("../mail/%s/%s" % (echo, msg_file))

def make_toss():
    lst = [x for x in os.listdir("../base/out") if x.endswith(".out")]
    for msg in lst:
        text = codecs.open("../base/out/%s" % msg, "r", "utf-8").read()
        coded_text = base64.urlsafe_b64encode(text.encode("utf-8"))
        codecs.open("../base/out/%s.toss" % msg, "w", "utf-8").write(coded_text.decode("utf-8"))
        os.rename("../base/out/%s" % msg, "../base/out/%s%s" % (msg, "msg"))

def send_mail():
    lst = [x for x in os.listdir("../base/out") if x.endswith(".toss")]
    for msg in lst:
        text = codecs.open("../base/out/%s" % msg, "r", "utf-8").read()
        result = urllib.request.urlopen("%su/point/%s/%s"% (ii.node, ii.auth, text)).read().decode("utf-8")
        if result.startswith("msg ok"):
            os.remove("../base/out/%s" % msg)
        elif result == "msg big!":
            print ("ERROR: very big message (limit 64K)!")
        elif result == "auth error!":
            print ("ERROR: unknown auth!")
        else:
            print ("ERROR: unknown error!")

ii.load_config()
find_new()
make_toss()
send_mail()
