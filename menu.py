import configparser
from dialog import Dialog

config = configparser.ConfigParser()
config.read("config.ini")

if config["MOTOR"]["motorEnabled"] == "True":
    from motor import Motor

if config["FAN"]["fanEnabled"] == "True":
    from fan import Fan

if config["CAMERA"]["cameraEnabled"] == "True":
    from camera import Camera

class Menu():
    def __init__(self):
        self.d = Dialog(dialog="dialog")
        self.d.set_background_title(config["GENERAL"]["carName"])

        self.code = self.d.OK

        if config["MOTOR"]["motorEnabled"] == "True":
            self.motor = Motor(config)

        if config["FAN"]["fanEnabled"] == "True":
            self.fan = Fan(config)

        if config["CAMERA"]["cameraEnabled"] == "True":
            self.camera = Camera(config)
            self.camera.start()


    def go(self):
        while self.code == self.d.OK:
            self.code, self.tag = self.d.menu("Que puis-je faire pour vous ?",       #code = d.OK ou d.CANCEL
                               choices=[("(1)", "Gérer la direction"),              #tag = (1), ...
                                        ("(2)", "Gérer les moteurs"),
                                        ("(3)", "Gérer la caméra"),
                                        ("(4)", "Gérer les ventilateurs"),
                                        ("(5)", "Gérer la lampe")])

            if self.tag == "(1)" and config["MOTOR"]["motorEnabled"] == "True":
                code, tag = self.d.menu("Où voulez vous aller ?",
                                   choices=[("(1)", "Avancer"),
                                            ("(2)", "Reculer"),
                                            ("(3)", "Tourner à gauche"),
                                            ("(4)", "Tourner à droite")])

                self.motor.changeDirection(tag)

            elif self.tag == "(2)" and config["MOTOR"]["motorEnabled"] == "True":
                code, tag = self.d.menu("Que voulez vous faire avec vos moteurs ?",
                                   choices=[("(1)", "Allumé"),
                                            ("(2)", "Éteind")])

                self.motor.changeStatus(tag)

            elif self.tag == "(3)" and config["CAMERA"]["cameraEnabled"] == "True":
                code, tag = self.d.menu("Que voulez vous faire avec votre caméra ,",
                                   choices=[("(1)", "Allumé"),
                                            ("(2)", "Éteind"),
                                            ("(3)", "Récupérer le nombre d'image")])

                if tag != "(3)":
                    self.camera.setStatus(tag)
                else:
                    self.d.msgbox("Votre voiture à pris "+str(self.camera.getPhotoNb())+" photo(s)")

            elif self.tag == "(4)" and config["FAN"]["fanEnabled"] == "True":
                code, tag = self.d.menu("Que voulez vous faire avec vos ventilateurs ,",
                                   choices=[("(1)", "Allumé"),
                                            ("(2)", "Éteind")])

                self.fan.changeStatus(tag)

            elif self.tag == "(5)" and config["LAMP"]["lampEnabled"] == "True":
                code, tag = self.d.menu("Que voulez vous faire avec votre lampe ,",
                                   choices=[("(1)", "Allumé"),
                                            ("(2)", "Éteind")])

            elif self.tag != "":
                self.d.msgbox("Votre action a été désactivé dans la congiguration")

        self.camera.stop()
        self.motor.changeStatus("(2)")
        self.fan.changeStatus("(2)")
