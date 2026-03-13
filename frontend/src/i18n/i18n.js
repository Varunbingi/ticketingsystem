import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// safely get saved language
const savedLang = localStorage.getItem("lang") || "en";

const resources = {
  en: {
    translation: {
      signup: "Sign Up",
      login: "Login",
      logout: "Logout",
      home: "Home",
      tickets: "Tickets",
      username: "Username",
      password: "Password",
      notifications: "Notifications",
      language: "Language",

      users: "Users",
      client: "Client",
      roles: "Roles",
      permissions: "Permissions",

      // common UI
      add: "Add",
      id: "ID",
      name: "Name",
      description: "Description",
      actions: "Actions",

      // Users page
      users_page_title: "Users",
      no_users_found: "No users found",
      staff: "Staff",

      // Roles page
      role_name: "Role Name",
      short_name: "Short Name",
      no_roles: "No roles added",

      // Permissions page
      add_permission: "Add Permission",
      add_permission_category: "Add Permission Category",
      no_permissions: "No permissions added",

      // Tickets page
      tickets_page_title: "Tickets",
      subject: "Subject",
      priority: "Priority",
      status: "Status",
      low: "Low",
      medium: "Medium",
      high: "High",
      todo: "Todo",
      in_progress: "In Progress",
      done: "Done",

      // signup/login form
      firstname: "First Name",
      lastname: "Last Name",
      email: "Email",
      phone: "Phone",
      department: "Department ID",
      reporting_to: "Reporting To",
      suspended: "Suspended",
      deleted: "Deleted",
      creating_account: "Creating account…",
      or_signup_with: "OR SIGN UP WITH",
      already_have_account: "Already have an account?",

      // Notifications page
      loading_alerts: "Loading your alerts...",
      notification_description: "Updates regarding your tickets and account security.",
      notification_load_error: "Could not load notifications. Please try again later.",
      no_notifications: "No notifications yet",
      notification_wait: "We'll let you know when something happens.",
      mark_read: "Mark as read",
      new: "New"
    }
  },

  te: {
    translation: {
      signup: "సైన్ అప్",
      login: "లాగిన్",
      logout: "లాగౌట్",
      home: "హోమ్",
      tickets: "టికెట్లు",
      username: "యూజర్ పేరు",
      password: "పాస్వర్డ్",
      notifications: "నోటిఫికేషన్లు",
      language: "భాష",

      users: "వినియోగదారులు",
      client: "క్లయింట్",
      roles: "పాత్రలు",
      permissions: "అనుమతులు",

      add: "జోడించు",
      id: "ఐడి",
      name: "పేరు",
      description: "వివరణ",
      actions: "చర్యలు",

      users_page_title: "వినియోగదారులు",
      no_users_found: "వినియోగదారులు లేరు",
      staff: "సిబ్బంది",

      role_name: "పాత్ర పేరు",
      short_name: "చిన్న పేరు",
      no_roles: "పాత్రలు ఇంకా జోడించలేదు",

      add_permission: "అనుమతి జోడించు",
      add_permission_category: "అనుమతి వర్గం జోడించు",
      no_permissions: "ఇంకా అనుమతులు జోడించలేదు",

      tickets_page_title: "టికెట్లు",
      subject: "విషయం",
      priority: "ప్రాధాన్యత",
      status: "స్థితి",
      low: "తక్కువ",
      medium: "మధ్యస్థ",
      high: "అధిక",
      todo: "చేయవలసినవి",
      in_progress: "ప్రక్రియలో",
      done: "పూర్తైంది",

      firstname: "మొదటి పేరు",
      lastname: "చివరి పేరు",
      email: "ఈమెయిల్",
      phone: "ఫోన్",
      department: "డిపార్ట్‌మెంట్ ఐడి",
      reporting_to: "ఎవరికి రిపోర్ట్ చేస్తారు",
      suspended: "సస్పెండ్ చేయబడింది",
      deleted: "తొలగించబడింది",
      creating_account: "ఖాతా సృష్టిస్తోంది…",
      or_signup_with: "లేదా వీటితో సైన్ అప్ చేయండి",
      already_have_account: "ఇప్పటికే ఖాతా ఉందా?",

      loading_alerts: "మీ అలర్ట్స్ లోడ్ అవుతున్నాయి...",
      notification_description: "మీ టికెట్లు మరియు ఖాతా భద్రతకు సంబంధించిన అప్డేట్లు.",
      notification_load_error: "నోటిఫికేషన్లు లోడ్ చేయలేకపోయాం. దయచేసి తరువాత ప్రయత్నించండి.",
      no_notifications: "ఇప్పటివరకు నోటిఫికేషన్లు లేవు",
      notification_wait: "ఏదైనా జరిగినప్పుడు మేము మీకు తెలియజేస్తాము.",
      mark_read: "చదివినట్లు గుర్తించండి",
      new: "కొత్తవి"
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: savedLang,
    fallbackLng: "en",
    interpolation: {
      escapeValue: false
    },
    react: {
      useSuspense: false
    }
  });

// sync language with localStorage
i18n.on("languageChanged", (lng) => {
  localStorage.setItem("lang", lng);
});

export default i18n;