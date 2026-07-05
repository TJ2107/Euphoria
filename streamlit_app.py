import streamlit as st
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Dict
from uuid import UUID, uuid4
from datetime import datetime
import numpy as np

# Simplified, self-contained Streamlit port of the EUPHORIA demo

st.set_page_config(page_title="EUPHORIA — Bonheur App", layout="wide")

# -----------------------------
# Data classes and core logic
# -----------------------------

@dataclass
class EtatEmotionnel:
    user_id: UUID = field(default_factory=uuid4)
    bonheur: float = 0.5
    energie: float = 0.5
    stress: float = 0.5
    connexion_sociale: float = 0.5
    sens_vie: float = 0.5
    gratitude: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)
    contexte: str = ""


@dataclass
class ProfilUtilisateur:
    user_id: UUID = field(default_factory=uuid4)
    nom: str = ""
    age: int = 25
    centres_interet: List[str] = field(default_factory=list)
    valeurs: List[str] = field(default_factory=list)
    objectifs_vie: List[str] = field(default_factory=list)
    etat_emotionnel_actuel: EtatEmotionnel = field(default_factory=EtatEmotionnel)
    historique_emotionnel: List[EtatEmotionnel] = field(default_factory=list)
    score_bonheur_baseline: float = 0.5
    cercle_social: List[UUID] = field(default_factory=list)
    activites_positives_count: int = 0


class TypeMessage(IntEnum):
    TEXTE = 1
    VOIX = 2
    VIDEO = 3
    PHOTO = 4
    EXPRESSION_GRATITUDE = 5
    PARTAGE_REUSSITE = 6
    SOUTIEN_EMOTIONNEL = 7
    MOMENT_PRESENT = 8
    COURAGE_ENVOYE = 9
    QUESTION_PROFONDE = 10


class MessengerProfond:
    def __init__(self):
        self.conversations: Dict[str, List[dict]] = {}

    def envoyer_message(self, expediteur: UUID, destinataire: str, contenu: str, type_msg: TypeMessage) -> Dict:
        msg = {
            'id': str(uuid4()),
            'expediteur': str(expediteur),
            'destinataire': destinataire,
            'contenu': contenu,
            'type': int(type_msg),
            'timestamp': datetime.now().isoformat(),
            'reactions': [],
            'impact_bonheur': self._calculer_impact_bonheur(contenu, type_msg)
        }
        # store conversation
        key = f"{expediteur}:{destinataire}"
        self.conversations.setdefault(key, []).append(msg)

        suggestions = self._generer_suggestions(contenu, type_msg)
        profondeur = self._evaluer_profondeur(contenu)

        return {
            'message': msg,
            'suggestions_profondeur': suggestions,
            'score_profondeur': profondeur
        }

    def _generer_suggestions(self, contenu: str, type_msg: TypeMessage) -> List[str]:
        suggestions = []
        contenu_lower = contenu.lower()
        if '?' in contenu:
            suggestions.extend([
                "💭 Qu'est-ce qui t'a fait penser à ça ?",
                "❤️ Comment te sens-tu par rapport à ça ?",
                "🌟 Qu'est-ce que tu aimerais qu'il se passe ?"
            ])
        elif 'triste' in contenu_lower or 'mal' in contenu_lower:
            suggestions.extend([
                "💙 Je suis là pour toi",
                "🤗 Qu'est-ce qui t'aiderait en ce moment ?",
                "🌈 Qu'est-ce qui te ferait du bien ?"
            ])
        elif 'heureux' in contenu_lower or 'joie' in contenu_lower:
            suggestions.extend([
                "🎉 Célébrons ce moment !",
                "📸 Partage un souvenir de ce bonheur",
                "🙏 Qu'est-ce pour lequel tu es reconnaissant ?"
            ])
        else:
            suggestions.extend([
                "💭 Qu'est-ce que ça t'inspire ?",
                "🌟 Raconte-moi en plus",
                "❤️ Qu'est-ce qui compte le plus pour toi ?"
            ])
        return suggestions[:3]

    def _evaluer_profondeur(self, contenu: str) -> float:
        score = 0.5
        mots_profonds = ['penser', 'ressentir', 'croire', 'rêver', 'espérer', 'aimer', 'vivre', 'sens', 'valeur', 'passion']
        mots_superficiels = ['ok', 'cool', 'lol', 'mdr', 'slt', 'cc']
        contenu_lower = contenu.lower()
        for mot in mots_profonds:
            if mot in contenu_lower:
                score += 0.1
        for mot in mots_superficiels:
            if mot in contenu_lower:
                score -= 0.15
        return float(np.clip(score, 0.0, 1.0))

    def _calculer_impact_bonheur(self, contenu: str, type_msg: TypeMessage) -> float:
        if type_msg in [TypeMessage.EXPRESSION_GRATITUDE, TypeMessage.PARTAGE_REUSSITE, TypeMessage.SOUTIEN_EMOTIONNEL, TypeMessage.MOMENT_PRESENT]:
            return 0.15
        elif type_msg == TypeMessage.QUESTION_PROFONDE:
            return 0.12
        else:
            return 0.05 * self._evaluer_profondeur(contenu)


class Contenu:
    def __init__(self, titre: str, type_contenu: int, tags: List[str], score_bonheur_predit: float = 0.5, duree_sec: int = 30):
        self.id = str(uuid4())
        self.titre = titre
        self.type_contenu = type_contenu
        self.tags = tags
        self.score_bonheur_predit = score_bonheur_predit
        self.duree_sec = duree_sec
        self.genere_interaction = True
        self.createur = "EUPHORIA"
        self.positif_certifie = True


class FeedPositif:
    def __init__(self, profil: ProfilUtilisateur):
        self.profil = profil
        self.contenus: List[Contenu] = []
        self.historique_visionnage: List[str] = []
        # seed sample contents
        self._seed_contents()

    def _seed_contents(self):
        samples = [
            ("Respire: 2 minutes pour apaiser le stress", 6, ["respiration", "apaisant"], 0.8, 45),
            ("Petites victoires: célébrer aujourd'hui", 8, ["gratitude", "victoire"], 0.9, 20),
            ("Balade en nature : vidéo relaxante", 6, ["nature", "calme"], 0.85, 60),
            ("Histoire d'entraide locale qui inspire", 10, ["connexion", "entraide"], 0.75, 90),
            ("Apprends une chose nouvelle en 3 min", 2, ["apprentissage"], 0.6, 180)
        ]
        for t, typ, tags, score, dur in samples:
            self.contenus.append(Contenu(t, typ, tags, score, dur))

    def generer_feed_personnalise(self, n_contenus: int = 5) -> List[Contenu]:
        contenus_scores = []
        for contenu in self.contenus:
            if contenu.id in self.historique_visionnage:
                continue
            score = self._calculer_score_bonheur(contenu)
            contenus_scores.append((contenu, score))
        contenus_scores.sort(key=lambda x: x[1], reverse=True)
        return [c for c, s in contenus_scores[:n_contenus]]

    def _calculer_score_bonheur(self, contenu: Contenu) -> float:
        pertinence = self._calculer_pertinence(contenu)
        impact = contenu.score_bonheur_predit
        diversite = 1.0
        match_emotionnel = 0.7
        if self.profil.etat_emotionnel_actuel.stress > 0.7:
            if contenu.type_contenu in [6, 1, 10]:
                match_emotionnel = 1.0
            else:
                match_emotionnel = 0.3
        score_sante = 1.0 if len(self.historique_visionnage) < 20 else 0.5
        bonus_interaction = 0.2 if contenu.genere_interaction else 0
        score = (
            0.25 * pertinence +
            0.30 * impact +
            0.15 * diversite +
            0.15 * match_emotionnel +
            0.10 * score_sante +
            0.05 * (1 + bonus_interaction)
        )
        return float(np.clip(score, 0.0, 1.0))

    def _calculer_pertinence(self, contenu: Contenu) -> float:
        interets = set(self.profil.centres_interet)
        tags = set(contenu.tags)
        if not interets or not tags:
            return 0.5
        intersection = interets & tags
        return len(intersection) / len(interets) if interets else 0.5


class IAEmotionnelle:
    def __init__(self, profil: ProfilUtilisateur):
        self.profil = profil
        self.modele_emotionnel = self._initialiser_modele()

    def _initialiser_modele(self):
        return {
            'facteurs_bonheur': {
                'connexion_sociale': 0.40,
                'sens_vie': 0.25,
                'gratitude': 0.15,
                'energie': 0.10,
                'reduction_stress': 0.10
            }
        }

    def analyser_etat(self, interactions: List[Dict]) -> EtatEmotionnel:
        etat = EtatEmotionnel(user_id=self.profil.user_id)
        score_sentiment = 0.5
        for inter in interactions[-20:]:
            if inter.get('sentiment') == 'positif':
                score_sentiment += 0.02
            elif inter.get('sentiment') == 'negatif':
                score_sentiment -= 0.02
        etat.bonheur = float(np.clip(score_sentiment, 0.0, 1.0))
        etat.energie = 0.6
        etat.stress = 0.3
        etat.connexion_sociale = 0.5
        etat.sens_vie = 0.5
        etat.gratitude = 0.5
        return etat

    def recommander_intervention(self) -> Dict:
        etat = self.profil.etat_emotionnel_actuel
        scores_facteurs = {
            'connexion_sociale': etat.connexion_sociale,
            'sens_vie': etat.sens_vie,
            'gratitude': etat.gratitude,
            'energie': etat.energie
        }
        facteur_faible = min(scores_facteurs, key=scores_facteurs.get)
        interventions_map = {
            'connexion_sociale': {
                'action': "💬 Envoie un message à quelqu'un que tu apprécies",
                'pourquoi': "La connexion sociale est le 1er facteur de bonheur",
                'duree': "2 min",
                'impact_bonheur': 0.15
            },
            'gratitude': {
                'action': "🙏 Note 3 choses pour lesquelles tu es reconnaissant",
                'pourquoi': "La gratitude augmente le bonheur",
                'duree': "3 min",
                'impact_bonheur': 0.12
            },
            'sens_vie': {
                'action': "🌟 Fais une activité alignée avec tes valeurs",
                'pourquoi': "Le sens est essentiel au bonheur durable",
                'duree': "20 min",
                'impact_bonheur': 0.20
            },
            'energie': {
                'action': "⚡ Bouge 10 min ou prends l'air",
                'pourquoi': "L'énergie physique booste l'humeur",
                'duree': "10 min",
                'impact_bonheur': 0.10
            }
        }
        return interventions_map[facteur_faible]

    def alerte_bien_etre(self) -> Dict:
        etat = self.profil.etat_emotionnel_actuel
        if etat.bonheur < 0.2 and etat.stress > 0.8:
            return {
                'niveau': 'URGENT',
                'message': "💙 On sent que ça va pas. Voici des ressources :",
                'ressources': [
                    "📞 3114 (numéro national prévention suicide)",
                    "👨‍⚕️ Consulter médecin ou psychologue",
                    "🤝 Parler à un proche de confiance",
                    "🧘 Respiration 4-7-8 (inspire 4s, bloque 7s, expire 8s)"
                ]
            }
        elif etat.bonheur < 0.35:
            return {
                'niveau': 'ATTENTION',
                'message': "💙 On est là pour vous. Quelques suggestions :",
                'ressources': [
                    "🎯 Faire une activité qui vous plaît",
                    "👥 Contacter un proche",
                    "📝 Journal de gratitude"
                ]
            }
        return {}


class ImpactSocialReel:
    def __init__(self, profil: ProfilUtilisateur):
        self.profil = profil
        self.actions_realisees = []
        self.impact_mesure = {
            'heures_benevolat': 0,
            'argent_donne': 0.0,
            'personnes_aidees': 0,
            'co2_evite_kg': 0.0,
            'sourires_offerts': 0,
            'score_impact_total': 0.0
        }

    def suggerer_actions_proches(self, localisation: str = "Paris"):
        return [
            {
                'type': 1,
                'titre': "🍽️ Servir repas aux sans-abri",
                'organisation': "Restos du Cœur",
                'distance_km': 1.2,
                'duree_heures': 2,
                'impact_personnes': 30,
                'benefice_personnel': "Sens + connexion + gratitude",
                'lien_inscription': "https://..."
            },
            {
                'type': 3,
                'titre': "🛒 Faire courses pour personne âgée",
                'organisation': "Voisins Solidaires",
                'distance_km': 0.3,
                'duree_heures': 1,
                'impact_personnes': 1,
                'benefice_personnel': "Lien social + utilité",
                'lien_inscription': "https://..."
            }
        ]

    def enregistrer_action(self, action_data: Dict):
        action = {
            'id': str(uuid4()),
            'user_id': str(self.profil.user_id),
            'type': action_data['type'],
            'titre': action_data['titre'],
            'date': datetime.now().isoformat(),
            'duree_heures': action_data.get('duree_heures', 0),
            'impact_personnes': action_data.get('impact_personnes', 0),
            'photo_preuve': action_data.get('photo'),
            'benefice_personnel_ressenti': action_data.get('ressenti', '')
        }
        self.actions_realisees.append(action)
        # mise à jour simplifiée
        if action['type'] == 1:
            self.impact_mesure['heures_benevolat'] += action['duree_heures']
            self.impact_mesure['personnes_aidees'] += action['impact_personnes']
        elif action['type'] == 3:
            self.impact_mesure['personnes_aidees'] += action['impact_personnes']
        self.impact_mesure['score_impact_total'] = (
            self.impact_mesure['heures_benevolat'] * 10 +
            self.impact_mesure['argent_donne'] * 0.1 +
            self.impact_mesure['personnes_aidees'] * 5
        )
        return {'action': action, 'impact_mesure': self.impact_mesure}


class EUPHORIA:
    def __init__(self, nom_utilisateur: str = "Utilisateur"):
        self.profil = ProfilUtilisateur(nom=nom_utilisateur)
        self.messenger = MessengerProfond()
        self.feed = FeedPositif(self.profil)
        self.ia_emotionnelle = IAEmotionnelle(self.profil)
        self.impact_social = ImpactSocialReel(self.profil)
        self.profil.historique_emotionnel.append(self.profil.etat_emotionnel_actuel)

    def demarrer_session(self):
        return self.profil.etat_emotionnel_actuel


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("💖 EUPHORIA — L'application qui vise votre bonheur")

# Sidebar: user settings
st.sidebar.header("Profil")
username = st.sidebar.text_input("Nom", value="Sophie")
centres = st.sidebar.text_input("Centres d'intérêt (virgule séparés)", value="nature,gratitude,respiration")
if 'app_instance' not in st.session_state:
    st.session_state.app_instance = EUPHORIA(username)
    st.session_state.app_instance.profil.centres_interet = [c.strip() for c in centres.split(',') if c.strip()]

app: EUPHORIA = st.session_state.app_instance

# Update profile name if changed
if username != app.profil.nom:
    app.profil.nom = username

col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Votre état émotionnel")
    etat = app.demarrer_session()
    st.metric("Bonheur", f"{etat.bonheur:.0%}")
    st.metric("Énergie", f"{etat.energie:.0%}")
    st.metric("Stress", f"{etat.stress:.0%}")
    st.write(f"Connexion sociale: {etat.connexion_sociale:.2f}")
    st.write(f"Sens de vie: {etat.sens_vie:.2f}")
    st.write(f"Gratitude: {etat.gratitude:.2f}")

    # Intervention recommandée
    intervention = app.ia_emotionnelle.recommander_intervention()
    st.subheader("Suggestion du jour")
    st.write(f"**{intervention['action']}**")
    st.write(f"{intervention['pourquoi']} • {intervention['duree']}")
    if st.button("Accepter l'intervention"):
        app.profil.activites_positives_count += 1
        st.success("✨ Intervention acceptée — bravo !")

    alert = app.ia_emotionnelle.alerte_bien_etre()
    if alert:
        st.error(alert['message'])
        for r in alert['ressources']:
            st.write(r)

with col2:
    st.subheader("Messenger Profond")
    with st.form("message_form"):
        destinataire = st.text_input("Destinataire", value="Maman")
        message = st.text_area("Message")
        type_choice = st.selectbox("Type de message", options=[(m.name, m.value) for m in TypeMessage], format_func=lambda x: x[0])
        submitted = st.form_submit_button("Envoyer")
        if submitted and message.strip():
            # find TypeMessage by name
            tm = TypeMessage[type_choice[0]] if isinstance(type_choice, tuple) else TypeMessage.TEXTE
            resultat = app.messenger.envoyer_message(app.profil.user_id, destinataire, message, tm)
            # apply impact to profile bonheur (simple)
            impact = resultat['message']['impact_bonheur']
            app.profil.etat_emotionnel_actuel.bonheur = float(np.clip(app.profil.etat_emotionnel_actuel.bonheur + impact, 0.0, 1.0))
            app.profil.historique_emotionnel.append(app.profil.etat_emotionnel_actuel)
            st.success(f"Message envoyé — Profondeur: {resultat['score_profondeur']:.0%} — Impact bonheur +{impact:.0%}")
            st.write("Suggestions :")
            for s in resultat['suggestions_profondeur']:
                st.write(f"- {s}")

    st.subheader("Feed positif")
    contenus = app.feed.generer_feed_personnalise(5)
    for c in contenus:
        with st.expander(c.titre):
            st.write(f"Score bonheur prédit: {c.score_bonheur_predit:.0%}")
            st.write(f"Durée: {c.duree_sec}s")
            if st.button(f"Marquer comme vu: {c.titre}", key=c.id):
                app.feed.historique_visionnage.append(c.id)
                st.success("Contenu marqué comme vu")

st.markdown("---")

st.subheader("Impact social réel")
suggestions = app.impact_social.suggerer_actions_proches()
for i, action in enumerate(suggestions, 1):
    cols = st.columns([4,1])
    with cols[0]:
        st.write(f"**{action['titre']}** — {action['organisation']} ({action['distance_km']} km)")
        st.write(f"⏱️ {action['duree_heures']}h • Impact: {action['impact_personnes']} personnes")
        st.write(action['benefice_personnel'])
    with cols[1]:
        if st.button(f"Je participe ({i})", key=f"participe_{i}"):
            res = app.impact_social.enregistrer_action(action)
            st.success("Merci ! Action enregistrée")
            st.write(res['impact_mesure'])

st.markdown("---")

st.subheader("Bilan de session")
if st.button("Afficher le bilan"):
    impact = app.impact_social.impact_mesure
    st.write(f"Heures bénévolat: {impact['heures_benevolat']}")
    st.write(f"Argent donné: {impact['argent_donne']}€")
    st.write(f"Personnes aidées: {impact['personnes_aidees']}")
    st.write(f"CO2 évité: {impact['co2_evite_kg']} kg")
    st.write(f"Score impact: {impact['score_impact_total']}")
    if len(app.profil.historique_emotionnel) > 1:
        bonheur_init = app.profil.historique_emotionnel[0].bonheur
        bonheur_actuel = app.profil.etat_emotionnel_actuel.bonheur
        st.write(f"Évolution bonheur: {bonheur_init:.2f} → {bonheur_actuel:.2f}")

st.caption("Version simplifiée Streamlit de la démo EUPHORIA — conçue pour exploration locale et prototype.")
