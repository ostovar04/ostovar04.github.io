/*
  Language and copy deck.
  Edit the fa/en strings here to change what visitors read.
  Markup stays in index.html; text with data-i18n="key" is replaced from this file.
*/
(function () {
  const copy = {
    fa: {
      navAbout: 'درباره', navSkills: 'توانایی‌ها', navProjects: 'پروژه‌ها', navTeam: 'همراهان', navChannels: 'آموزش', navMusic: 'موسیقی', navContact: 'ارتباط',
      themeToLight: 'روشن', themeToDark: 'تیره',
      heroEyebrow: 'متین · نمونه‌کار توسعهٔ نرم‌افزار', heroTitleA: 'هر حرکت،', heroTitleB: 'حساب‌شده است.',
      heroIntro: 'من متین هستم؛ دانشجوی مهندسی کامپیوتر و توسعه‌دهنده‌ای که روی تبدیل ایده‌ها به ابزارهای کاربردی کار می‌کند؛ از Python و Django تا هوش مصنوعی، Android و Unity.',
      heroRole: 'توسعه‌دهندهٔ نرم‌افزار · طراح وب', heroPrimary: 'دیدن پروژه‌ها', heroSecondary: 'پروفایل GitHub', heroScroll: 'برای ادامه، پایین برو ↓',
      aboutEyebrow: '01 / دربارهٔ من', aboutTitleA: 'ذهنی منطقی،', aboutTitleB: 'نگاهی سازنده.',
      aboutText: 'دانشجوی مهندسی کامپیوتر در دانشگاه آزاد اسلامی هستم. تمرکزم توسعهٔ بک‌اند با Python و Django، ساخت ایجنت‌های هوش مصنوعی، اپلیکیشن‌های Android و نمونه‌های Unity است. طراحی وب و فرانت‌اند را هم به‌صورت پروژه‌ای انجام می‌دهم و با تیمم در بازاریابی و تحویل پروژه همکاری می‌کنم.',
      factEducationLabel: 'تحصیلات', factEducation: 'مهندسی کامپیوتر · دانشگاه آزاد اسلامی', factFocusLabel: 'حوزهٔ تمرکز', factWorkLabel: 'شیوهٔ همکاری', factWork: 'پروژه‌ای و تیمی', factPrinciple: 'یادگیریِ پیوسته · ساختنِ کاربردی', aboutQuote: 'اول مشاهده؛ بعد یک حرکتِ دقیق.',
      skillsEyebrow: '02 / جعبه‌ابزار', skillsTitle: 'ابزارهایی برای ساختن', skillsIntro: 'این‌ها حوزه‌هایی هستند که در آن‌ها کار می‌کنم و با هر پروژه بیشتر یاد می‌گیرم.',
      skillBackend: 'توسعهٔ بک‌اند و ساخت API با تمرکز بر Python و Django.', skillAI: 'ساخت ایجنت‌های هوش مصنوعی و گردش‌کارهای کاربردی.', skillAndroid: 'ساخت اپلیکیشن‌های کاربردی برای پلتفرم Android.', skillUnity: 'نمونه‌سازی تعاملی و تجربه‌های بازی‌سازی.', skillWeb: 'طراحی وب و توسعهٔ فرانت‌اند به‌صورت پروژه‌ای.', skillDeliveryTitle: 'همکاری و تحویل پروژه', skillDelivery: 'همکاری با تیم در هماهنگی، بازاریابی و تحویل پروژه.',
      projectsEyebrow: '03 / پروژه‌ها', projectsTitle: 'از ایده تا اجرا', projectsIntro: 'وضعیت پروژهٔ منتشرشده و طرح‌های آینده را جداگانه آورده‌ام.', projectStatus: 'منتشرشده · پروژهٔ ۰۱', projectDescription: 'جست‌وجوی غذای فارسی و رستوران‌های اطراف روی نقشهٔ نشان؛ در شعاع ۵ کیلومتر و مرتب‌شده بر اساس فاصله.', liveDemo: 'دموی زنده', sourceCode: 'مخزن GitHub', roadmapTitle: 'ایده‌های آینده · هنوز منتشر نشده‌اند', planned: 'در برنامه',
      teamEyebrow: '04 / همراهان مسیر', teamTitle: 'همراهان مسیر', teamIntro: 'همراهانی با مهارت‌هایی مکمل و نگاهی سازنده.', nimaBio: 'هوش مصنوعی آفلاین و LLMها، اتوماسیون، بازی‌سازی و طراحی سه‌بعدی.', alirezaBio: 'توسعهٔ Python، زیرساخت Linux، امنیت سایبری و اتوماسیون هوش مصنوعی آفلاین.',
      channelsEyebrow: '05 / یادگیری و اشتراک‌گذاری', channelsTitle: 'یاد بگیریم، بسازیم، به‌اشتراک بگذاریم', channelsIntro: 'کانال‌های آموزشی NextGen AI & n8n دربارهٔ هوش مصنوعی محلی، ایجنت‌ها و اتوماسیون.', youtubeDescription: 'آموزش‌های ویدیویی دربارهٔ هوش مصنوعی محلی، ابزارها و اتوماسیون.', telegramDescription: 'خبرها، ابزارها و منابع مرتبط با AI محلی، n8n و پروژه‌های آموزشی.', channelOpen: 'رفتن به کانال',
      musicEyebrow: '06 / موسیقیِ پس‌زمینه', musicTitle: 'یک قطعهٔ اصیل با حال‌وهوای استراتژیک', musicText: 'ترکیبی از پدهای آرام و نت‌های پراکنده؛ برای لحظه‌هایی که تمرکز، فکر و یک حرکتِ دقیق لازم است.', musicPlay: 'پخش موسیقی', musicPause: 'توقف موسیقی', musicPlaying: 'موسیقی در حال پخش است.', musicPaused: 'پخش موسیقی متوقف شده است.',
      resumeEyebrow: 'رزومهٔ یک‌صفحه‌ای', resumeFa: 'دریافت نسخهٔ فارسی', resumeEn: 'دریافت نسخهٔ انگلیسی',
      contactEyebrow: '07 / ارتباط', contactTitle: 'برای ایدهٔ بعدی آماده‌ام.', contactIntro: 'برای همکاری، پروژهٔ وب یا گفت‌وگو دربارهٔ یک ایدهٔ نرم‌افزاری، از راه‌های زیر پیام بده.', emailLabel: 'ایمیل', formTitle: 'نوشتن پیام', formName: 'نام', formEmail: 'ایمیل شما', formMessage: 'پیام', formSend: 'بازکردن ایمیل برای ارسال', formOpened: 'برنامهٔ ایمیل با پیام آماده باز شد.', formSubject: 'پیام از وب‌سایت متین', mailName: 'نام', mailAddress: 'ایمیل', mailMessage: 'پیام', formError: 'برای نوشتن پیام، یک برنامهٔ ایمیل روی دستگاه لازم است؛ می‌توانی مستقیم به نشانی بالا ایمیل بزنی.',
      footerLine: 'ساختنِ خوب، با یک حرکتِ سنجیده شروع می‌شود.', backTop: 'بازگشت به بالا'
    },
    en: {
      navAbout: 'About', navSkills: 'Toolkit', navProjects: 'Projects', navTeam: 'Allies', navChannels: 'Learn', navMusic: 'Music', navContact: 'Contact',
      themeToLight: 'Light', themeToDark: 'Dark',
      heroEyebrow: 'MATIN · SOFTWARE PORTFOLIO', heroTitleA: 'EVERY MOVE,', heroTitleB: 'CONSIDERED.',
      heroIntro: 'I’m Matin, a computer engineering student and developer focused on turning ideas into useful tools—from Python and Django to AI agents, Android, and Unity.',
      heroRole: 'SOFTWARE DEVELOPER · WEB DESIGNER', heroPrimary: 'Explore projects', heroSecondary: 'GitHub profile', heroScroll: 'SCROLL TO EXPLORE ↓',
      aboutEyebrow: '01 / ABOUT', aboutTitleA: 'A LOGICAL MIND,', aboutTitleB: 'A BUILDER’S EYE.',
      aboutText: 'I study Computer Engineering at Islamic Azad University. My focus includes Python and Django back-end development, AI agents, Android apps, and Unity prototypes. I also take on freelance web and front-end design, and work with my team on marketing and project delivery.',
      factEducationLabel: 'EDUCATION', factEducation: 'Computer Engineering · Islamic Azad University', factFocusLabel: 'FOCUS', factWorkLabel: 'WORK MODE', factWork: 'Freelance & team', factPrinciple: 'Keep learning · Build useful things', aboutQuote: 'Observe first. Then make the right move.',
      skillsEyebrow: '02 / TOOLKIT', skillsTitle: 'Tools for building', skillsIntro: 'These are the areas I work in and keep learning through each project.',
      skillBackend: 'Back-end development and API building with a focus on Python and Django.', skillAI: 'Building AI agents and practical automation workflows.', skillAndroid: 'Creating useful applications for Android.', skillUnity: 'Interactive prototyping and game-development experiences.', skillWeb: 'Freelance web design and front-end development.', skillDeliveryTitle: 'Collaboration & delivery', skillDelivery: 'Working with the team on coordination, marketing, and project delivery.',
      projectsEyebrow: '03 / PROJECTS', projectsTitle: 'From idea to release', projectsIntro: 'The released project is separated from concepts that are still planned.', projectStatus: 'PUBLISHED · PROJECT 01', projectDescription: 'Discover Persian food and nearby restaurants on the Neshan map, within a 5 km radius and sorted by distance.', liveDemo: 'Live demo', sourceCode: 'GitHub repository', roadmapTitle: 'Upcoming concepts · not released', planned: 'PLANNED',
      teamEyebrow: '04 / COLLABORATORS', teamTitle: 'People along the way', teamIntro: 'Creative collaborators with complementary skills and a shared drive to build.', nimaBio: 'Offline AI and LLMs, automation, game development, and 3D design.', alirezaBio: 'Python development, Linux infrastructure, cybersecurity, and offline-AI automation.',
      channelsEyebrow: '05 / LEARNING & SHARING', channelsTitle: 'Learn, build, share', channelsIntro: 'NextGen AI & n8n tutorials on local AI, agents, and automation.', youtubeDescription: 'Video tutorials about local AI, useful tools, and automation.', telegramDescription: 'Updates, tools, and resources for local AI, n8n, and learning projects.', channelOpen: 'Open channel',
      musicEyebrow: '06 / BACKGROUND MUSIC', musicTitle: 'An original track with a strategic mood', musicText: 'Soft ambient layers and scattered notes for moments that call for focus, reflection, and a deliberate move.', musicPlay: 'Play music', musicPause: 'Pause music', musicPlaying: 'Background music is playing.', musicPaused: 'Background music is paused.',
      resumeEyebrow: 'ONE-PAGE RESUME', resumeFa: 'Persian PDF', resumeEn: 'English PDF',
      contactEyebrow: '07 / CONTACT', contactTitle: 'Ready for the next idea.', contactIntro: 'For collaboration, a web project, or a conversation about a software idea, use one of the options below.', emailLabel: 'EMAIL', formTitle: 'Write a message', formName: 'Name', formEmail: 'Your email', formMessage: 'Message', formSend: 'Open email to send', formOpened: 'Your email app should open with the message prepared.', formSubject: 'Message from Matin’s website', mailName: 'Name', mailAddress: 'Email', mailMessage: 'Message', formError: 'An email app is needed to send this message. You can email the address shown above directly.',
      footerLine: 'Good work begins with a considered move.', backTop: 'Back to top'
    }
  };

  const app = window.APP = window.APP || {};
  app.copy = copy;
  app.lang = document.documentElement.lang === 'en' ? 'en' : 'fa';
  app.t = function (key) { return (copy[app.lang] && copy[app.lang][key]) || key; };
  app.setLanguage = function (language) {
    if (!copy[language]) return;
    app.lang = language;
    document.documentElement.lang = language;
    document.documentElement.dir = language === 'fa' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-i18n]').forEach(function (node) {
      const key = node.getAttribute('data-i18n');
      if (copy[language][key]) node.textContent = copy[language][key];
    });
    const button = document.getElementById('language-toggle');
    if (button) {
      button.textContent = language === 'fa' ? 'EN' : 'فا';
      button.setAttribute('aria-label', language === 'fa' ? 'Switch to English' : 'تغییر زبان به فارسی');
    }
    document.title = language === 'fa' ? 'متین | هر حرکت، حساب‌شده' : 'Matin | Every Move, Considered';
    window.dispatchEvent(new CustomEvent('site-language-change', { detail: { language: language } }));
  };

  document.documentElement.classList.remove('no-js');
  document.documentElement.classList.add('js');
  const languageButton = document.getElementById('language-toggle');
  if (languageButton) languageButton.addEventListener('click', function () {
    app.setLanguage(app.lang === 'fa' ? 'en' : 'fa');
  });
  app.setLanguage(app.lang);
})();
