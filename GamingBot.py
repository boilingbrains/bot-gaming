import requests #lib pour la partie web scraping
from bs4 import BeautifulSoup #lib  pour la  partie web scraping
import smtplib #lib pour la partie email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER =  "smtp.gmail.com" #Serveur email
SMTP_PORT = 587 #Port du serveur
GMAIL_USERNAME  = #Votre adresse  email
GMAIL_PASSWORD = #Votre  mot de passe
receiverAddress = #Adresse mail destinataire

emailSubject = "Rapport du bot gaming \U0001F3AE" #Objet du email 
emailBase = "C'est le moment d'acheter :\n\n" #Début du corps du email
emailContent = "" #Contenu du mail
emailSignature = "\n Cordialement,\n Le bot" #Signature du mail
sendEmail = False #Variable de contrôle permettant de savoir s'il faut envoyer l'email

#Liste des URLs des jeux dont je souhaite surveiller le prix
games_urls = [
"https://www.instant-gaming.com/fr/4824-acheter-elden-ring-pc-jeu-steam-europe/",   
"https://www.instant-gaming.com/fr/7110-acheter-ghostwire-tokyo-pc-jeu-steam-europe/",
"https://www.instant-gaming.com/fr/10386-acheter-tiny-tina-s-wonderlands-edition-merveilleux-chaos-chaotic-great-edition-pc-jeu-epic-games-europe/",
"https://www.instant-gaming.com/fr/2075-acheter-ready-or-not-early-access-pc-jeu-steam/",
]

#Liste des prix en dessous desquels je souhaite être notifié pour chaque jeu
prices_thresholds = [35.00, 30.00, 40.00, 30.00]

#Listes dans lesquelles on stockera nom et prix des jeux
games_names = [""]*len(games_urls)
games_prices = [""]*len(games_urls)

#Boucle qui parcourt la liste des URLs et qui récupère le nom et le prix de chaque jeu
for i in range(len(games_urls)):
    page = requests.get(games_urls[i])
    parser = BeautifulSoup(page.content,'html.parser')
    games_names[i] = parser.find(class_="game-title").text
    games_prices[i] = parser.find_all(class_="total")[1].text
 
#Boucle qui vérifie si le prix récupéré pour chaque jeu est inférieur au prix souhaité
#Si c'est le cas on rajoute le nom et le prix du jeu à acheter dans le contenu de l'email à envoyer
for j in range (len(games_names)):
    if(float(games_prices[j][:-1]) < prices_thresholds[j]):
        emailContent = emailContent + "\U0001F539" + games_names[j] + " [" + games_prices[j] + "]\n"
        sendEmail = True

#Envoi de l'email
if(sendEmail == True):
    #Le corps du mail est composé de la phrase de base, des noms des jeux à acheter et de la signature
    emailBody = emailBase + emailContent + emailSignature

    #Creation de  l'email
    message = MIMEMultipart()
    message['From'] = GMAIL_USERNAME
    message['To'] = receiverAddress
    message['Subject'] = emailSubject
    message.attach(MIMEText(emailBody, 'plain'))

    #Connexion  au serveur Gmail
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
 
    #Authentification
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    #Envoi de l'email
    session.sendmail(GMAIL_USERNAME, receiverAddress, message.as_string())
    session.quit
    
    #Le mail vient d'être envoyé, on remet la variable de controle à False
    sendEmail = False
