/**
 * Comprehensive Multi-Language Localization Engine (i18n)
 * Supports: English, Hindi (हिन्दी), Telugu (తెలుగు), Tamil (தமிழ்), Bengali (বাংলা), Marathi (मराठी)
 */

const TRANSLATIONS = {
  en: {
    nav_dashboard: "Dashboard",
    nav_ocr: "Report OCR",
    nav_summary: "Health Summary",
    nav_profile: "Unified Profile",
    nav_abdm: "ABDM & Regimes",
    nav_login: "Sign In",
    nav_register: "Register / Create ABHA",
    nav_logout: "Sign Out",

    hero_title: "Unified Digital Health Vault & ABDM Portal",
    hero_subtitle: "Your intelligent personal health cockpit. Understand clinical lab reports instantly, access your official ABDM ABHA Card, and manage digital health regimes in your preferred language.",
    
    ocr_title: "Medical Report OCR & Biomarker Scanner",
    ocr_desc: "Upload lab tests, diagnostic scans, or prescription documents. Our dual-layer AI instantly extracts numerical biomarkers, validates reference ranges, and flags abnormal metrics.",
    ocr_drag_drop: "Drag & drop your medical lab report image here, or browse files",
    ocr_supported_formats: "Supported formats: JPG, PNG, WEBP (Max 16 MB)",
    ocr_load_preset: "Or click a sample test panel to test instantly:",
    ocr_btn_scan: "Run Diagnostic OCR Scan",
    ocr_scanning: "Scanning Document & Extracting Biomarkers...",
    
    table_parameter: "Biomarker / Test",
    table_value: "Result",
    table_range: "Normal Reference Range",
    table_status: "Clinical Status",
    table_notes: "What It Means",

    summary_title: "Plain-Language Health Explainer",
    summary_subtitle: "Doctor-to-Human translation of your medical tests into crystal-clear everyday words.",
    summary_overview: "Overall Health Snapshot",
    summary_attention: "What Needs Your Attention",
    summary_lifestyle: "Daily Nutrition & Lifestyle Tips",
    summary_questions: "Questions to Ask Your Doctor",

    profile_title: "Unified Health Profile & Vitals",
    profile_subtitle: "Your consolidated personal health record (PHR) and emergency medical ID.",
    vitals_bp: "Blood Pressure",
    vitals_glucose: "Blood Glucose",
    vitals_heart: "Heart Rate",
    vitals_spo2: "Oxygen (SpO2)",
    vitals_bmi: "Body Mass Index",
    medications_title: "Active Prescriptions & Medications",
    allergies_title: "Documented Allergies & Sensitivities",
    conditions_title: "Chronic Health Conditions",

    abdm_title: "Ayushman Bharat Digital Mission (ABDM)",
    abdm_subtitle: "Official ABHA Health Card & Digital Consent Regime Manager",
    abdm_flip_hint: "Click to Flip Card (Front / Back)",
    abdm_download: "Download Card",
    abdm_print: "Print ABHA Card",
    abdm_regimes_title: "ABDM Health Regimes & Consent Manager",
    abdm_regimes_desc: "Control which hospitals, diagnostic labs, and clinicians can access your health data.",
    abdm_facility: "Facility / Clinician",
    abdm_purpose: "Consent Purpose",
    abdm_validity: "Valid Until",
    abdm_status: "Permission Status",
    abdm_action: "Action"
  },

  hi: {
    nav_dashboard: "डैशबोर्ड",
    nav_ocr: "रिपोर्ट ओसीआर",
    nav_summary: "स्वास्थ्य सारांश",
    nav_profile: "एकीकृत प्रोफ़ाइल",
    nav_abdm: "आभा कार्ड एवं शासन",
    nav_login: "लॉग इन करें",
    nav_register: "पंजीकरण / आभा बनाएं",
    nav_logout: "लॉग आउट",

    hero_title: "एकीकृत डिजिटल स्वास्थ्य वॉल्ट एवं आभा पोर्टल",
    hero_subtitle: "आपका व्यक्तिगत स्मार्ट स्वास्थ्य केंद्र। मेडिकल रिपोर्ट को सरल भाषा में समझें, अपना आधिकारिक आभा कार्ड प्राप्त करें और अपनी भाषा में स्वास्थ्य रिकॉर्ड प्रबंधित करें।",

    ocr_title: "मेडिकल रिपोर्ट ओसीआर एवं बायोमार्कर स्कैनर",
    ocr_desc: "लैब रिपोर्ट या पर्ची अपलोड करें। हमारा एआई सिस्टम तुरंत परीक्षण परिणामों को पहचानकर सामान्य व असामान्य मानों को हाइलाइट करता है।",
    ocr_drag_drop: "अपनी मेडिकल रिपोर्ट की फोटो यहाँ खींचें या फ़ाइल चुनें",
    ocr_supported_formats: "समर्थित प्रारूप: JPG, PNG, WEBP (अधिकतम 16 MB)",
    ocr_load_preset: "या तुरंत परीक्षण के लिए नमूना रिपोर्ट चुनें:",
    ocr_btn_scan: "ओसीआर परीक्षण शुरू करें",
    ocr_scanning: "दस्तावेज़ स्कैन हो रहा है...",

    table_parameter: "परीक्षण / बायोमार्कर",
    table_value: "परिणाम मान",
    table_range: "सामान्य सीमा",
    table_status: "स्वास्थ्य स्थिति",
    table_notes: "इसका क्या अर्थ है",

    summary_title: "सरल भाषा में स्वास्थ्य रिपोर्ट सारांश",
    summary_subtitle: "कठिन मेडिकल शब्दों को आसान और समझने योग्य भाषा में अनुवादित किया गया।",
    summary_overview: "समग्र स्वास्थ्य स्थिति",
    summary_attention: "इन बातों पर विशेष ध्यान दें",
    summary_lifestyle: "आहार एवं जीवनशैली सुझाव",
    summary_questions: "डॉक्टर से पूछने योग्य प्रश्न",

    profile_title: "एकीकृत स्वास्थ्य प्रोफ़ाइल एवं वाइटल्स",
    profile_subtitle: "आपका केंद्रीय स्वास्थ्य रिकॉर्ड एवं आपातकालीन मेडिकल पहचान।",
    vitals_bp: "रक्तचाप (BP)",
    vitals_glucose: "रक्त शर्करा (शुगर)",
    vitals_heart: "हृदय गति (पल्स)",
    vitals_spo2: "ऑक्सीजन स्तर (SpO2)",
    vitals_bmi: "बॉडी मास इंडेक्स (BMI)",
    medications_title: "सक्रिय दवाइयाँ",
    allergies_title: "एलर्जी एवं संवेदनशीलता",
    conditions_title: "पुरानी स्वास्थ्य स्थितियाँ",

    abdm_title: "आयुष्मान भारत डिजिटल मिशन (ABDM)",
    abdm_subtitle: "आधिकारिक आभा (ABHA) कार्ड एवं डिजिटल सहमति प्रबंधक",
    abdm_flip_hint: "कार्ड पलटने के लिए क्लिक करें",
    abdm_download: "कार्ड डाउनलोड करें",
    abdm_print: "कार्ड प्रिंट करें",
    abdm_regimes_title: "स्वास्थ्य रिकॉर्ड शेयरिंग एवं सहमति नियंत्रण",
    abdm_regimes_desc: "नियंत्रित करें कि कौन सा अस्पताल या लैब आपके रिकॉर्ड देख सकता है।",
    abdm_facility: "अस्पताल / चिकित्सक",
    abdm_purpose: "सहमति का उद्देश्य",
    abdm_validity: "वैधता तिथि",
    abdm_status: "सहमति स्थिति",
    abdm_action: "कार्रवाई"
  },

  te: {
    nav_dashboard: "డ్యాష్‌బోర్డ్",
    nav_ocr: "రిపోర్ట్ OCR",
    nav_summary: "ఆరోగ్య సారాంశం",
    nav_profile: "సమగ్ర ప్రొఫైల్",
    nav_abdm: "ABDM & ఆభా కార్డ్",
    nav_login: "లాగిన్",
    nav_register: "నమోదు / ఆభా సృష్టించండి",
    nav_logout: "లాగ్ అవుట్",

    hero_title: "సమగ్ర డిజిటల్ హెల్త్ వాల్ట్ & ABDM పోర్టల్",
    hero_subtitle: "మీ స్మార్ట్ వ్యక్తిగత ఆరోగ్య కేంద్రం. వైద్య నివేదికలను సులభంగా అర్థం చేసుకోండి, మీ అధికారిక ఆభా కార్డును పొందండి మరియు మీ మాతృభాషలోనే రికార్డులను నిర్వహించండి.",

    ocr_title: "వైద్య నివేదిక OCR & బయోమార్కర్ స్కానర్",
    ocr_desc: "మీ ల్యాబ్ రిపోర్టును అప్‌లోడ్ చేయండి. AI క్షణాల్లో ఫలితాలను విశ్లేషించి సాధారణ మరియు అసాధారణ విలువలను గుర్తిస్తుంది.",
    ocr_drag_drop: "మెడికల్ రిపోర్ట్ చిత్రాన్ని ఇక్కడ వేయండి లేదా ఫైల్ ఎంచుకోండి",
    ocr_supported_formats: "అనుమతించబడినవి: JPG, PNG, WEBP (గరిష్టంగా 16 MB)",
    ocr_load_preset: "లేదా వెంటనే పరీక్షించడానికి నమూనా రిపోర్ట్ ఎంచుకోండి:",
    ocr_btn_scan: "రిపోర్ట్ స్కాన్ ప్రారంభించండి",
    ocr_scanning: "పత్రం స్కాన్ అవుతోంది...",

    table_parameter: "పరీక్ష / బయోమార్కర్",
    table_value: "ఫలితం విలువ",
    table_range: "సాధారణ పరిమితి",
    table_status: "స్థితి",
    table_notes: "దీని అర్థం ఏమిటి",

    summary_title: "సులభమైన భాషలో ఆరోగ్య సారాంశం",
    summary_subtitle: "క్లిష్టమైన వైద్య పదాలను సులువైన మాటల్లో వివరించబడింది.",
    summary_overview: "మొత్తం ఆరోగ్య స్థితి",
    summary_attention: "మీరు శ్రద్ధ వహించాల్సిన అంశాలు",
    summary_lifestyle: "ఆహారం & జీవనశైలి సూచనలు",
    summary_questions: "వైద్యుడిని అడగవలసిన ప్రశ్నలు",

    profile_title: "సమగ్ర ఆరోగ్య ప్రొఫైల్ & వైటల్స్",
    profile_subtitle: "మీ వ్యక్తిగత ఆరోగ్య రికార్డు మరియు అత్యవసర గుర్తింపు.",
    vitals_bp: "రక్తపోటు (BP)",
    vitals_glucose: "బ్లడ్ షుగర్",
    vitals_heart: "గుండె వేగం",
    vitals_spo2: "ఆక్సిజన్ (SpO2)",
    vitals_bmi: "శరీర బరువు సూచిక (BMI)",
    medications_title: "ప్రస్తుత మందులు",
    allergies_title: "అలెర్జీలు",
    conditions_title: "దీర్ఘకాలిక సమస్యలు",

    abdm_title: "ఆయుష్మాన్ భారత్ డిజిటల్ మిషన్ (ABDM)",
    abdm_subtitle: "అధికారిక ఆభా (ABHA) కార్డ్ & డిజిటల్ సమ్మతి మేనేజర్",
    abdm_flip_hint: "కార్డును తిప్పడానికి క్లిక్ చేయండి",
    abdm_download: "కార్డ్ డౌన్‌లోడ్ చేయండి",
    abdm_print: "కార్డ్ ప్రింట్ చేయండి",
    abdm_regimes_title: "ఆరోగ్య రికార్డు సమ్మతి నిర్వహణ",
    abdm_regimes_desc: "మీ ఆరోగ్య రికార్డులను ఏ ఆసుపత్రి చూడవచ్చో నియంత్రించండి.",
    abdm_facility: "ఆసుపత్రి / ల్యాబ్",
    abdm_purpose: "ఉద్దేశం",
    abdm_validity: "చెల్లుబాటు తేదీ",
    abdm_status: "సమ్మతి స్థితి",
    abdm_action: "చర్య"
  },

  ta: {
    nav_dashboard: "முகப்பு",
    nav_ocr: "அறிக்கை OCR",
    nav_summary: "சுகாதார சுருக்கம்",
    nav_profile: "முழு சுயவிவரம்",
    nav_abdm: "ABDM ஆபா அட்டை",
    nav_login: "உள்நுழைவு",
    nav_register: "பதிவு செய்க",
    nav_logout: "வெளியேறு",

    hero_title: "ஒருங்கிணைந்த டிஜிட்டல் சுகாதார தளம் & ABDM",
    hero_subtitle: "மருத்துவ பரிசோதனை அறிக்கைகளை எளிதாக புரிந்து கொள்ளுங்கள், அதிகாரப்பூர்வ ஆபா அட்டையைப் பெறுங்கள்.",

    ocr_title: "மருத்துவ அறிக்கை OCR & ஸ்கேனர்",
    ocr_drag_drop: "உங்கள் மருத்துவ அறிக்கையை இங்கே பதிவேற்றவும்",
    table_parameter: "பரிசோதனை பெயர்",
    table_value: "முடிவு",
    table_range: "இயல்பான அளவு",
    table_status: "நிலை",

    summary_title: "எளிய மொழியில் அறிக்கை சுருக்கம்",
    summary_overview: "ஒட்டுமொத்த சுகாதார நிலை",
    summary_attention: "கவனிக்க வேண்டியவை",
    summary_lifestyle: "உணவு மற்றும் வாழ்க்கை முறை குறிப்புகள்",
    summary_questions: "மருத்துவரிடம் கேட்க வேண்டிய கேள்விகள்",

    abdm_title: "ஆயுஷ்மான் பாரத் டிஜிட்டல் மிஷன் (ABDM)",
    abdm_download: "அட்டையைப் பதிவிறக்குக",
    abdm_print: "அச்சிடுக"
  },

  bn: {
    nav_dashboard: "ড্যাশবোর্ড",
    nav_ocr: "রিপোর্ট OCR",
    nav_summary: "স্বাস্থ্য সারাংশ",
    nav_profile: "ইউনিফাইড প্রোফাইল",
    nav_abdm: "ABDM আভা কার্ড",
    nav_login: "লগইন",
    nav_register: "নিবন্ধন করুন",
    nav_logout: "লগআউট",

    hero_title: "ইউনিফাইড ডিজিটাল হেলথ ভল্ট ও আভা পোর্টাল",
    hero_subtitle: "আপনার মেডিকেল টেস্ট রিপোর্ট সহজ ভাষায় বুঝুন এবং অফিসিয়াল আভা কার্ড পান।",

    ocr_title: "মেডিকেল রিপোর্ট OCR স্ক্যানার",
    table_parameter: "পরীক্ষার নাম",
    table_value: "ফলাফল",
    table_range: "স্বাভাবিক মাত্রা",
    table_status: "অবস্থা",

    summary_title: "সহজ ভাষায় স্বাস্থ্য রিপোর্ট",
    summary_overview: "সামগ্রিক স্বাস্থ্য অবস্থা",
    summary_attention: "যে বিষয়গুলিতে নজর দেওয়া প্রয়োজন",
    summary_lifestyle: "খাবার ও জীবনযাত্রার পরামর্শ",
    summary_questions: "ডাক্তারকে জিজ্ঞেস করার প্রশ্ন",

    abdm_title: "আয়ুষ্মান ভারত ডিজিটাল মিশন (ABDM)",
    abdm_download: "কার্ড ডাউনলোড করুন",
    abdm_print: "প্রিন্ট করুন"
  },

  mr: {
    nav_dashboard: "डॅशबोर्ड",
    nav_ocr: "रिपोर्ट ओसीआर",
    nav_summary: "आरोग्य सारांश",
    nav_profile: "युनिफाइड प्रोफाइल",
    nav_abdm: "आभा कार्ड व व्यवस्था",
    nav_login: "लॉग इन",
    nav_register: "नोंदणी करा",
    nav_logout: "लॉग आउट",

    hero_title: "डिजिटल हेल्थ व्हॉल्ट आणि आभा पोर्टल",
    hero_subtitle: "वैद्यकीय अहवाल सोप्या भाषेत समजून घ्या आणि आपले अधिकृत आभा कार्ड मिळवा.",

    ocr_title: "वैद्यकीय अहवाल ओसीआर स्कॅनर",
    table_parameter: "चाचणी",
    table_value: "निकाल",
    table_range: "सामान्य श्रेणी",
    table_status: "स्थिती",

    summary_title: "सोप्या भाषेत आरोग्य सारांश",
    summary_overview: "एकूण आरोग्य स्थिती",
    summary_attention: "विशेष लक्ष देण्याच्या बाबी",
    summary_lifestyle: "आहार आणि जीवनशैली टिप्स",
    summary_questions: "डॉक्टरांना विचारण्याचे प्रश्न",

    abdm_title: "आयुष्मान भारत डिजिटल मिशन (ABDM)",
    abdm_download: "कार्ड डाउनलोड करा",
    abdm_print: "प्रिंट करा"
  }
};

class I18nManager {
  static currentLang = localStorage.getItem('hv_language') || 'en';

  static init() {
    this.applyLanguage(this.currentLang);
    this.bindLanguageSelectors();
  }

  static applyLanguage(lang) {
    if (!TRANSLATIONS[lang]) lang = 'en';
    this.currentLang = lang;
    localStorage.setItem('hv_language', lang);

    const strings = TRANSLATIONS[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (strings[key]) {
        el.innerText = strings[key];
      }
    });

    // Update active flag or dropdown title if present
    const langLabel = document.getElementById('current-lang-label');
    if (langLabel) {
      const names = { en: 'English', hi: 'हिन्दी', te: 'తెలుగు', ta: 'தமிழ்', bn: 'বাংলা', mr: 'मराठी' };
      langLabel.innerText = names[lang] || 'English';
    }
  }

  static bindLanguageSelectors() {
    document.querySelectorAll('.lang-select-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const lang = btn.getAttribute('data-lang');
        if (lang) {
          I18nManager.applyLanguage(lang);
          // Sync with server session
          fetch(`/set-language/${lang}`);
        }
      });
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  I18nManager.init();
});
