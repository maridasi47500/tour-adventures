from directory import Directory
from render_figure import RenderFigure
from mydb import Mydb
from scriptruby import Scriptruby


from mypic import Pic
from javascript import Js
from stylesheet import Css
import re
import traceback
import sys

class Route():
    def __init__(self):
        self.Program=Directory("trouve 1 ad ")
        self.Program.set_path("./")
        self.mysession={"notice":None,"email":None,"name":None}
        self.scriptruby=Scriptruby
        self.db = Mydb()
        self.render_figure=RenderFigure(self.Program)
        self.getparams=("id",)
    def set_post_data(self,x):
        self.post_data=x
    def get_post_data(self):
        return self.post_data
    def set_my_session(self,x):
        print("set session",x)
        self.Program.set_my_session(x)
        self.render_figure.set_session(self.Program.get_session())
    def get_exception_routes(self):
        #form n'est pas envoye avec javascript/jquery
        return ["/chercheradweb","/chercherad"]
    def get_some_post_data(self,params=()):
        #if route in  some routes
        x={}
        try:
            for y in params:
                print(self.post_data) #erreur
                print(self.post_data[y]) #erreur
                x[y]=self.post_data[y][0]
        except Exception as e:
            print("wow",e)
        return x
    def set_redirect(self,x):
        self.Program.set_redirect(x)
        self.render_figure.set_redirect(self.Program.get_redirect())
    def render_some_json(self,x):
        self.Program.set_json(True)
        return self.render_figure.render_some_json(x)
    def set_json(self,x):
        self.Program.set_json(x)
        self.render_figure.set_json(self.Program.get_json())
    def set_notice(self,x):
        print("set session",x)
        self.Program.set_session_params({"notice":x})
        self.render_figure.set_session(self.Program.get_session())
    def set_session(self,x):
        print("set session",x)
        self.Program.set_session(x)
        self.render_figure.set_session(self.Program.get_session())
    def get_this_route_param(self,x,params):
        print("set session",x)
        return dict(zip(x,params["routeparams"]))
    def logout(self,search):
        self.Program.logout()
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def welcome(self,search):
        hi=self.dbScript.getall()
        self.render_figure.set_param("scripts",hi)
        return self.render_figure.render_figure("welcome/allscript.html")
    def allscript(self,search):
        #myparam=self.get_post_data()(params=("name","content","monscript",))
        hi=self.dbScript.getall()
        self.render_figure.set_param("scripts",hi)
        return self.render_figure.render_figure("welcome/allscript.html")
    def hello(self,search):
        print("hello action")
        return self.render_figure.render_figure("welcome/index.html")
    def samecity(self,search={}):
        
        self.render_figure.set_params("sometext",self.Ad.samecity())
        return self.render_figure.render_figure("welcome/newad.html")
    def mysportjournal(self,search={}):
        
        self.render_figure.set_params("sometext",self.Ad.mysportjournal())
        return self.render_figure.render_figure("welcome/newad.html")
    def newad(self,search={}):
        self.render_figure.set_params("sometext","")
        return self.render_figure.render_figure("welcome/newad.html")
    def createad(self,params={}):
        myparams=self.get_post_data()(params=("name","lat","lon","description",))
        ad=self.db.Ad.create(myparams)
        if ad["ad_id"]:
          self.set_notice(ad["notice"])
          self.set_json("{\"redirect\":\"/voirad/"+ad["ad_id"]+"\"}")
        else:
          self.set_json("{\"redirect\":\"/\"}")
        return self.render_figure.render_json()
    def searchadweb(self,params={}):
        print("yay")
        myparams=self.get_some_post_data(params=("ad","lieu","rayon"))
        self.render_figure.set_param("s",(myparams["ad"] + " " +myparams["lieu"] + " dans un rayon de " + myparams["rayon"]+" km"))
        print("ad ::: ",myparams["ad"],myparams["lieu"])
        ok=self.db.Ad.getplacesnearby(myparams["ad"],myparams["lieu"])
        self.render_figure.set_param("ads",ok["rows"])
        self.render_figure.set_param("message",ok["message"])
        try:
            print("ad",myparams["ad"],myparams["lieu"])
            haha=self.scriptruby("ad",myparams["ad"],myparams["lieu"],myparams["rayon"]).lancer()
        except Exception as e:
            print(e)
        print(ok,"OHHHHHHH EHHHHHH")
        return self.render_figure.render_figure("welcome/searchad.html")
    def searchad(self,params={}):
        print("yay")
        myparams=self.get_some_post_data(params=("ad","lieu"))
        self.render_figure.set_param("s",(myparams["ad"] + " " +myparams["lieu"]))
        ok=self.db.Ad.getplacesnearby(myparams["ad"],myparams["lieu"])
        self.render_figure.set_param("ads",ok["rows"])
        self.render_figure.set_param("message",ok["message"])
        return self.render_figure.render_figure("welcome/searchad.html")
    def voirad(self,params={}):
        getparams=("id",)
        myparam=self.get_this_route_param(getparams,params)
        self.render_figure.set_param("ad",self.db.Ad.getbyid(myparam["id"]))
        return self.render_figure.render_figure("welcome/voirad.html")
    def voirtoutcequejaiajoute(self,data):

        print("tout")
        tout=self.db.Ad.getall()
        print("tout")
        print(tout,"tout")
        self.render_figure.set_param("tout",tout)
        return self.render_some_json("welcome/hey.json")
    def run(self,redirect=False,redirect_path=False,path=False,session=False,params={},url=False,post_data=False):
        if post_data:
            print("post data")
            self.set_post_data(post_data)
            print("post data set",post_data)
        if url:
            print("url : ",url)
            self.Program.set_url(url)
        self.set_my_session(session)

        if redirect:
            self.redirect=redirect
        if redirect_path:
            self.redirect_path=redirect
        if not self.render_figure.partie_de_mes_mots(balise="section",text=self.Program.get_title()):
            self.render_figure.ajouter_a_mes_mots(balise="section",text=self.Program.get_title())
        if path and path.endswith("png"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("html"):
            self.Program=Somehtml(path)
            self.Program.set_path("./")
        elif path and path.endswith("jpeg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("gif"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("svg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("jpg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith(".jfif"):
            self.Program=Pic(path)
        elif path and path.endswith(".css"):
            self.Program=Css(path)
        elif path and path.endswith(".js"):
            self.Program=Js(path)
        elif path:
            path=path.split("?")[0]
            print("OHHHHHH ")
            print("link route ",path)
            ROUTES={


                    '^/chercherad$': self.searchad,
                    '^/chercheradweb$': self.searchadweb,
                    '^/samecity$': self.samecity,
                    '^/mysportjournal$': self.mysportjournal,
                    '^/newad$': self.newad,
                    "^/voirad/([0-9]+)$":self.voirad,
                    '^/createad$': self.createad,
                    '^/toutcequejaiajoute$': self.voirtoutcequejaiajoute,
                    '^/allscript$': self.allscript,
                    '^/$': self.hello

                    }
            REDIRECT={"/save_user": "/welcome"}
            REDIRECT={"/save_user": "/welcome"}
            for route in ROUTES:
               print("pattern=",route)
               mycase=ROUTES[route]
               x=(re.match(route,path))
               print(True if x else False)
               #code bon pour les erreurs dans le code python
               if x:
                   params["routeparams"]=x.groups()
                   try:
                       html=mycase(params)
                   except Exception as e:
                       print("erreur"+str(e),traceback.format_exc())
                       html=("<p>une erreur s'est produite dans le code server  "+(traceback.format_exc())+"</p><a href=\"/\">retour à l'accueil</a>").encode("utf-8")
                       print(html)
                   self.Program.set_html(html=html)
                   self.Program.clear_notice()
                   return self.Program
               else:
                   self.Program.set_html(html="<p>la page n'a pas été trouvée</p><a href=\"/\">retour à l'accueil</a>")

        return self.Program
