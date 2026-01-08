import streamlit as st
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# Reading Passage Content
reading_passage_title = "Venezuela, Groenland : La politique de « prédation » de Donald Trump"
reading_passage_text = """Le week-end dernier, une opération militaire américaine spectaculaire a conduit à la capture du président vénézuélien, Nicolas Maduro, à Caracas. Emmené de force aux États-Unis, cet événement marque une escalade majeure de la politique étrangère de Donald Trump. Au mépris total du droit international, cette action est perçue par de nombreux observateurs comme l'affirmation d'une puissance américaine agressive, qui ne cache plus ses véritables motivations : le contrôle des ressources. L'épisode a choqué le monde entier et soulève des questions inquiétantes sur l'avenir des relations internationales.
Pour justifier cette intervention, l'administration américaine met en avant la lutte contre le narcotrafic. Nicolas Maduro est présenté comme un « narcoterroriste » à la tête d'un réseau criminel. Cependant, les experts invités par Mediapart expliquent que cet argument est principalement un prétexte. Le Venezuela n'est ni un producteur majeur de cocaïne, ni la principale source des drogues qui causent des ravages aux États-Unis. Cette justification permet surtout à Washington de présenter son action comme une opération de police plutôt qu'une guerre, évitant ainsi certaines procédures légales et politiques complexes sur le plan national.
La véritable motivation, selon les analystes, est une pure logique de prédation économique. Dans ses déclarations, Donald Trump ne parle jamais de démocratie, mais insiste sur le pétrole. Le Venezuela possède les plus grandes réserves de pétrole au monde (17 % du total mondial), et les compagnies américaines souhaitent en reprendre le contrôle. Cette stratégie vise à s'assurer un accès direct et sécurisé aux matières premières, dans un contexte de rivalité croissante avec la Chine. Il ne s'agit plus de promouvoir un modèle politique, mais de garantir les intérêts économiques bruts des États-Unis.
Cette politique agressive s'inscrit dans le cadre d'une version réactualisée de la « Doctrine Monroe », une théorie du XIXe siècle qui considérait l'Amérique latine comme l'« arrière-cour » des États-Unis. Donald Trump y ajoute ce que les experts appellent un « corollaire Trump » : une version encore plus directe et brutale, où la diplomatie est remplacée par la force. Le slogan du Département d'État américain, « This is our hemisphere » (« Ceci est notre hémisphère »), résume parfaitement cette vision impériale. Les autres pays, y compris les alliés européens, sont perçus comme des vassaux qui doivent se soumettre.
L'intervention au Venezuela n'est d'ailleurs qu'un début. Donald Trump a déjà désigné ses prochaines cibles. Il menace directement la Colombie, met la pression sur le Mexique et prédit l'effondrement de Cuba. Mais ses ambitions dépassent le continent américain. Il a réaffirmé son désir d'acquérir le Groenland, un territoire danois stratégique riche en ressources naturelles. Cette menace directe envers un pays membre de l'OTAN et de l'Union Européenne montre que personne n'est à l'abri de cette logique impériale.
Face à cette démonstration de force, la réaction des dirigeants européens a été jugée extrêmement faible, voire lâche. Le président français Emmanuel Macron a d'abord salué la chute de la « dictature » de Maduro, sans mentionner la violation du droit international, une déclaration immédiatement repartagée par Donald Trump. Si certains pays comme l'Espagne ont plus clairement condamné l'opération, l'Europe apparaît divisée et incapable de formuler une réponse forte. Prise en tenaille entre l'impérialisme de Trump et celui de Poutine, l'Europe peine à défendre sa souveraineté et les principes d'un ordre mondial basé sur le droit.
"""

# Page configuration
st.set_page_config(page_title="Fransızca Okuma Sınavı", page_icon="🇫🇷")

# Configure Gemini API
try:
    api_key = st.secrets["general"]["GEMINI_API_KEY"]
    if api_key == "YOUR_API_KEY_HERE":
        st.error("Lütfen .streamlit/secrets.toml dosyasındaki API anahtarını güncelleyin.")
        st.stop()
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API anahtarı yapılandırma hatası: {e}")
    st.stop()

# Custom CSS for styling
st.markdown("""
    <style>
    .reading-box {
        background-color: #f0f2f6;
        color: #31333F;
        border-left: 5px solid #4e8cff;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        font-size: 1.1em;
        font-family: 'Georgia', serif;
    }
    .question-box {
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo_new.png", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Fransızca Okuduğunu Anlama</h1>", unsafe_allow_html=True)

# Reading Passage
st.markdown("<h2 style='text-align: center;'>Okuma Parçası</h2>", unsafe_allow_html=True)
st.markdown("""
    <div class="reading-box">
        <h3>Venezuela, Groenland : La politique de « prédation » de Donald Trump</h3>
        <p></p>
        <p>Le week-end dernier, une opération militaire américaine spectaculaire a conduit à la capture du président vénézuélien, Nicolas Maduro, à Caracas. Emmené de force aux États-Unis, cet événement marque une escalade majeure de la politique étrangère de Donald Trump. Au mépris total du droit international, cette action est perçue par de nombreux observateurs comme l'affirmation d'une puissance américaine agressive, qui ne cache plus ses véritables motivations : le contrôle des ressources. L'épisode a choqué le monde entier et soulève des questions inquiétantes sur l'avenir des relations internationales.</p>
        <p>Pour justifier cette intervention, l'administration américaine met en avant la lutte contre le narcotrafic. Nicolas Maduro est présenté comme un « narcoterroriste » à la tête d'un réseau criminel. Cependant, les experts invités par Mediapart expliquent que cet argument est principalement un prétexte. Le Venezuela n'est ni un producteur majeur de cocaïne, ni la principale source des drogues qui causent des ravages aux États-Unis. Cette justification permet surtout à Washington de présenter son action comme une opération de police plutôt qu'une guerre, évitant ainsi certaines procédures légales et politiques complexes sur le plan national.</p>
        <p>La véritable motivation, selon les analystes, est une pure logique de prédation économique. Dans ses déclarations, Donald Trump ne parle jamais de démocratie, mais insiste sur le pétrole. Le Venezuela possède les plus grandes réserves de pétrole au monde (17 % du total mondial), et les compagnies américaines souhaitent en reprendre le contrôle. Cette stratégie vise à s'assurer un accès direct et sécurisé aux matières premières, dans un contexte de rivalité croissante avec la Chine. Il ne s'agit plus de promouvoir un modèle politique, mais de garantir les intérêts économiques bruts des États-Unis.</p>
        <p>Cette politique agressive s'inscrit dans le cadre d'une version réactualisée de la « Doctrine Monroe », une théorie du XIXe siècle qui considérait l'Amérique latine comme l'« arrière-cour » des États-Unis. Donald Trump y ajoute ce que les experts appellent un « corollaire Trump » : une version encore plus directe et brutale, où la diplomatie est remplacée par la force. Le slogan du Département d'État américain, « This is our hemisphere » (« Ceci est notre hémisphère »), résume parfaitement cette vision impériale. Les autres pays, y compris les alliés européens, sont perçus comme des vassaux qui doivent se soumettre.</p>
        <p>L'intervention au Venezuela n'est d'ailleurs qu'un début. Donald Trump a déjà désigné ses prochaines cibles. Il menace directement la Colombie, met la pression sur le Mexique et prédit l'effondrement de Cuba. Mais ses ambitions dépassent le continent américain. Il a réaffirmé son désir d'acquérir le Groenland, un territoire danois stratégique riche en ressources naturelles. Cette menace directe envers un pays membre de l'OTAN et de l'Union Européenne montre que personne n'est à l'abri de cette logique impériale.</p>
        <p>Face à cette démonstration de force, la réaction des dirigeants européens a été jugée extrêmement faible, voire lâche. Le président français Emmanuel Macron a d'abord salué la chute de la « dictature » de Maduro, sans mentionner la violation du droit international, une déclaration immédiatement repartagée par Donald Trump. Si certains pays comme l'Espagne ont plus clairement condamné l'opération, l'Europe apparaît divisée et incapable de formuler une réponse forte. Prise en tenaille entre l'impérialisme de Trump et celui de Poutine, l'Europe peine à défendre sa souveraineté et les principes d'un ordre mondial basé sur le droit.</p>
    </div>
""", unsafe_allow_html=True)

# Questions
st.subheader("Sorular")
questions = [
    "**1.** Pourquoi le gouvernement américain a-t-il officiellement arrêté Maduro, et quelle est la véritable raison économique liée aux ressources du pays ?",
    "**2.** Qu’est-ce que la « Doctrine Monroe » et comment Donald Trump l’utilise-t-il pour justifier son autorité sur l’Amérique latine ?",
    "**3.** Quelles sont les autres cibles de Donald Trump (en dehors du Venezuela) et pourquoi la réaction des pays européens a-t-elle été critiquée ?",
]

user_answers = []
for q in questions:
    user_answers.append(st.text_input(q, key=q))

# Check Answers Button
if st.button("Cevaplarımı Kontrol Et"):
    # Check if all fields are filled (optional, but good for UX)
    if not any(user_answers):
        st.warning("Lütfen en az bir soruya cevap verin.")
    else:
        with st.spinner("Öğretmen cevaplarınızı kontrol ediyor..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-pro')
                
                prompt = f"""
                Sen bir Fransızca öğretmenisin, yalnızca Fransızca cevap ver. Aşağıdaki okuma parçasına göre öğrencinin verdiği cevapları kontrol et.
                
                Okuma Parçası:
                "{reading_passage_title}"
                "{reading_passage_text}"
                
                Sorular ve Öğrenci Cevapları:
                """
                
                for i, (q, a) in enumerate(zip(questions, user_answers)):
                    prompt += f"\nSoru: {q}\nCevap: {a if a else 'Boş bırakıldı'}\n"
                
                prompt += """
                Lütfen her soru için:
                1. Cevabın doğruluğunu (içerik olarak) kontrol et, eğer cevap doğru değilse doğru cevabı ver. 
                2. Dilbilgisi hatası varsa bunları teker teker belirt ve doğrusunu açıkla.
                3. Her sorunun cevabını ve dilbilgisi hatasını ayrı ayrı yazdır.
                
                Önemli: Cevaplarını ve genel değerlendirmeni doğrudan öğrenciye hitap ederek yap ("sen" dili kullan). Örneğin "Cevabın doğru", "Şurada hata yapmışsın" gibi. Öğrenciyle konuşuyormuş gibi samimi ve teşvik edici ol.
                
                Yanıtın nazik ve öğretici bir dille olsun.
                """
                
                response = model.generate_content(prompt)
                st.session_state.evaluation_result = response.text
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")

if 'evaluation_result' not in st.session_state:
    st.session_state.evaluation_result = None

if st.session_state.evaluation_result:
    st.markdown("### Değerlendirme Sonucu")
    st.markdown(st.session_state.evaluation_result)
    
    st.markdown("---")
    st.subheader("Sonuçları Gönder")
    
    with st.form("email_form"):
        col_name, col_email, col_btn = st.columns([2, 2, 1])
        with col_name:
            student_name = st.text_input("İsim:", placeholder="Adınız Soyadınız")
        with col_email:
            student_email = st.text_input("E-mail:", placeholder="E-posta adresiniz")
        with col_btn:
            # Add some vertical spacing to align button with input
            st.write("") 
            st.write("")
            submitted = st.form_submit_button("Gönder")
            
        if submitted:
            if not student_name or not student_email:
                st.error("Lütfen isim ve e-posta alanlarını doldurun.")
            else:
                try:
                    sender_email = st.secrets["email"]["SENDER_EMAIL"]
                    password = st.secrets["email"]["SENDER_PASSWORD"]
                    teacher_email = "ilkerkocael@gmail.com"
                    recipients = [teacher_email, student_email]
                    
                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = ", ".join(recipients)
                    message["Subject"] = f"Fransızca Sınav Sonucu - {student_name}"
                    
                    # Format answers for email
                    answers_text = "\n".join([f"{q}\nCevap: {a}" for q, a in zip(questions, user_answers)])
                    
                    body = f"""
Öğrenci: {student_name}

--- Okuma Parçası ---
{reading_passage_title}
{reading_passage_text}

--- Sınav Cevapları ---
{answers_text}

--- Değerlendirme ---
{st.session_state.evaluation_result}
                    """
                    message.attach(MIMEText(body, "plain"))
                    
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, recipients, message.as_string())
                    
                    st.success(f"Sonuçlar {teacher_email} ve {student_email} adreslerine gönderildi!")
                except Exception as e:
                    st.error(f"E-posta gönderilirken hata oluştu: {e}")
                    st.info("Lütfen .streamlit/secrets.toml dosyasında e-posta ayarlarının doğru olduğundan emin olun.")
