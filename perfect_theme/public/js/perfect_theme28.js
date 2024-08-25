document.addEventListener('DOMContentLoaded', function() {
  function rotatimage(){
    // alert("dssd");
    var isRTL = getComputedStyle(document.body).direction === "rtl";
    var rtlImage = document.getElementById("rtl-image");
  
    if(document.getElementById("rtl-image")){
      if (isRTL) {
        rtlImage.style.transform = "rotate(180deg)";
      } else {
        rtlImage.style.transform = "rotate(0deg)";
      }
    }else{
      setTimeout(rotatimage, 500);
    }
    
  }
  function addCustombackGround() {
      // تحقق مما إذا كان شريط التنقل جاهزًا

      if (document.querySelector('.main-section')) {
          install();
          // إنشاء زر بدء التسجيل
          var startButton = document.createElement('img');
          startButton.innerHTML = '';
          startButton.src="/assets/perfect_theme/images/111.png";
          startButton.className = 'bg-ground';
          startButton.id = 'rtl-image';
          
          // إضافة الزر إلى شريط التنقل
          var container = document.querySelector('.main-section');
          container.insertBefore(startButton, container.firstChild);

          // إنشاء زر بدء التسجيل
          var startButton = document.createElement('div');
          startButton.innerHTML = '';
          startButton.className = 'overlay22';
          
          // إضافة الزر إلى شريط التنقل
          var container = document.querySelector('.main-section');
          container.insertBefore(startButton, container.firstChild);
          
      } else {
          // إذا لم يكن جاهزًا، تحقق مرة أخرى بعد 500 مللي ثانية
          setTimeout(addCustomButton, 500);
      }
  }

  function install() {
      // frappe.msgprint("sd");

      const apiUrl = 'perfect_theme.api.install';

      // إرسال طلب POST للـ API
      frappe.call({
          method: 'perfect_theme.api.install', // استدعاء الطريقة بشكل صحيح
          callback: function(response) {
              if (response.message) {
                  // التعامل مع البيانات المستلمة
                  console.log(response.message); // يمكن تغيير هذا لتناسب استخدامك
                  // frappe.msgprint(response.message); // عرض الرسالة في واجهة المستخدم
              }
          },
          error: function(error) {
              setTimeout(install, 500);
              console.error('فشل في الاتصال بالـ API:', error);
          }
      });
  }
// بدء المحاولة لإضافة الزر بعد تحميل الصفحة
setTimeout(addCustombackGround, 500);
setTimeout(rotatimage, 500);

// التفاعل عند النقر على زر بدء التسجيل


function Recording(){
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
const synth = window.speechSynthesis;

// وظيفة لتشغيل الرسالة الصوتية
function playArabicAudio(message,message_eng="") {
  // إنشاء utterance جديد
  lang="en-US";
  msg=message_eng;
  if(frappe.boot.lang=="ar"){
    lang = 'ar-SA';
    msg=message;
  }
  
  const utterance = new SpeechSynthesisUtterance(msg);

  utterance.lang=lang;
  // تعيين اللغة إلى العربية
  // utterance.lang = 'ar-SA';

  // تشغيل الرسالة الصوتية
  synth.speak(utterance);
}

// استخدام الوظيفة
// const arabicMessage = 'مرحبًا، هذه رسالة صوتية باللغة العربية.';
// playArabicAudio(arabicMessage);
// console.log(arabicMessage);
// إنشاء مثيل من واجهة التعرف على الصوت
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

// تعيين لغة التعرف إلى اللغة المناسبة
frappe.boot.lang;
if(frappe.boot.lang=="ar")
recognition.lang = 'ar-SU';
else
recognition.lang = 'en-US';

// التعرف على النص من الصوت
recognition.onresult = function(event) {
  var transcript = event.results[0][0].transcript;
  // البحث عن النص في الصفحة
  
  //   frappe.call({
  //     method: 'frappe.desk.search.search_widget',
  //     args: {
  //         doctype: '', // يمكنك تحديد نوع المستند الذي ترغب في البحث فيه إذا كان لديك نوع محدد
  //         txt: transcript,
  //         filters: {}  // يمكنك إضافة عوامل التصفية إذا كنت بحاجة
  //     },
  //     callback: function(response) {
  //         if (response.message) {
  //             // التعامل مع نتائج البحث
  //             console.log(response.message);
  //             // يمكنك عرض النتائج بطريقة تناسب تطبيقك
  //             frappe.msgprint({
  //                 message: JSON.stringify(response.message),
  //                 title: "نتائج البحث",
  //                 indicator: "green"
  //             });
  //         } else {
  //             frappe.msgprint({
  //                 message: "لم يتم العثور على نتائج",
  //                 title: "نتائج البحث",
  //                 indicator: "red"
  //             });
  //         }
  //     }
  // });
  document.getElementById("navbar-search").value=transcript;
  
  
  let index = transcript.indexOf("عرف عن نفسك");
  if(transcript.indexOf("عرف عن نفسك")!=-1 ){
    setTimeout(playArabicAudio("  انا نموذج ذكاء اصطناعي ذكي تم برمجتي من قبل شركة  الرؤيا الكاملة"), 500);
    return;
  }
  else if(transcript.indexOf("how are you")!=-1 || transcript.indexOf("كيف الحال")!=-1){
    setTimeout(playArabicAudio(" انا بخير. شكرا على سؤالك "," I am fine thank you"), 500);
    return;
  }
  else if(transcript.indexOf("who are you")!=-1){
    setTimeout(playArabicAudio(""," I am an intelligent artificial intelligence model that was programmed by perfect vision"), 500);
    return;
  }
  else if(transcript.indexOf("من انت")!=-1 ){
    setTimeout(playArabicAudio(" انا نموذج ذكاء اصطناعي ذكي تم برمجتي من قبل شركة الرؤيا الكاملة"), 500);
    return;
  }
  
  else if(transcript.indexOf("اشرح النظام")!=-1 || transcript.indexOf("عرفني على النظام")!=-1 || transcript.indexOf("عرفني بالنظام")!=-1 || transcript.indexOf("عرفني بهذا النظام")!=-1 ){
    var longText = `(erp alfras) هو نظام تخطيط موارد المؤسسة (ERP) مفتوح المصدر ويتميز بالمرونة والقوة. تم تطويره من قبل Alfras، وهي شركة برمجيات متخصصة في حلول ERP. (erp alfras) يغطي مجموعة واسعة من الوظائف الأساسية لإدارة الأعمال، بما في ذلك المحاسبة والمالية والمخزون والمشتريات والمبيعات والموارد البشرية. يتميز النظام بواجهة سهلة الاستخدام وأدوات تحليلية قوية تساعد في اتخاذ القرارات المستنيرة. إحدى المزايا الرئيسية لـ (erp alfras) هي قابليته للتخصيص والتكيف بسهولة مع متطلبات الأعمال المختلفة. يمكن للمستخدمين تخصيص العمليات والتقارير والواجهات وفقًا الحتياجاتهم الفردية. بالإضافة إلى ذلك، يتميز (erp alfras) بنموذج تسعير مرن وتكلفة ملكية منخفضة مقارنة بالحلول التجارية المغلقة. هذا يجعله خيارًا جذابًا للمؤسسات الصغيرة والمتوسطة والكبيرة على حد سواء. بشكل عام، (erp alfras) هو نظام ERP قوي ومفتوح المصدر يقدم حلاً شاملاً وقابلاً للتخصيص لإدارة جميع جوانب الأعمال.`;
    
    // تقسيم النص إلى جمل قصيرة
    var sentences = longText.match(/[^\.!\?]+[\.!\?]+/g);
    sentences.forEach(function(sentence) {
      playArabicAudio("",sentence);
      console.log(sentence);
      // setTimeout(, 500);
    });

    return;
  }
  else if(transcript.indexOf("Explain the system")!=-1 || transcript.indexOf("What is this system")!=-1 || transcript.indexOf("What is the system")!=-1  || transcript.indexOf("tell me about system")!=-1 || transcript.indexOf("tell me about the system")!=-1){
    var longText="erpalfras is a flexible and powerful open source ERP system. It was developed by Alfras, a software company specializing in ERP solutions. erpalfras covers a wide range of core business management functions, including accounting, finance, inventory, purchasing, sales and human resources. The system features an easy-to-use interface and powerful analytical tools that help in making informed decisions. One of the main advantages of erpalfras is its customizability and easy adaptation to different business requirements. Users can customize processes, reports, and interfaces according to their individual needs. In addition, erpalfras features a flexible pricing model and lower cost of ownership compared to closed commercial solutions. This makes it an attractive option for small, medium and large organizations alike. Overall, erpalfras is a powerful, open source ERP system that offers a comprehensive and customizable solution for managing all aspects of a business.";
    // تقسيم النص إلى جمل قصيرة
    var sentences = longText.match(/[^\.!\?]+[\.!\?]+/g);
    sentences.forEach(function(sentence) {
      playArabicAudio("",sentence);
      console.log(sentence);
      // setTimeout(, 500);
    });

    return;

  }
  transcript=transcript.replaceAll("العميل","عميل");
  transcript=transcript.replaceAll("العملاء","عميل");
  transcript=transcript.replaceAll("الموردون","مورد");
  transcript=transcript.replaceAll("المورد","مورد");
  transcript=transcript.replaceAll("واجهة","قائمة");
  transcript=transcript.replaceAll("افتح","");
  transcript=transcript.replaceAll("open","");
  transcript=transcript.replaceAll("interface","list");
  frappe.call({
    method:'alfrasgpt.api.search_and_open_interface',//'frappe.desk.search.search_link',
    args:{
      // doctype:"DocType",
      //txt:transcript,
      text:transcript,

    },
    callback:function(response){
      console.log(response)
      
      function getDomainName() {
        const url = new URL(window.location.href);
        return url.hostname;
      }
      if(response.message.Error=="true"){
        
        console.log('اسم النطاق:', getDomainName());
        window.location="https://"+getDomainName()+response.message.redirect;
        
        playArabicAudio("سيتم فتح الواجهة الان","Ok Dir."+frappe.session.user+". I will Open Interface Now");
      }
      else if(response.message.Error=="options"){
        console.log(response.message.results);
        var msg="<ol>";
        var m="";
        for (let i = 0; i < response.message.results.length; i++) {
          const element = response.message.results[i];
          var element_href=element.value.toLowerCase();
          m+=(i+1)+" "+element.value;
          element_href=element_href.replaceAll(" ","-");
          msg+="<li><a href='/app/"+element_href+"'> "+element.value +"</a></li>";
        }
        msg+="</ol>";

        var msg="هناك الكثير من الواجهات بهذا الاسم حدد اي من هذه الواجهات تريد"+msg;
        var msg_eng="There are many interfaces with this name. Select which of these interfaces you want"+msg;
        var msg_speach="هناك الكثير من الواجهات بهذا الاسم حدد اي من هذه الواجهات تريد"+m;
        var msg_speach_eng="There are many interfaces with this name. Select which of these interfaces you want"+m;
        msg=frappe.boot.lang=="ar"?msg:msg_eng;
        frappe.msgprint(msg);
        playArabicAudio(msg_speach,msg_speach_eng);
        Recording();
      }
      else{
        playArabicAudio(response.message.msg," Sorry I dont't find this interfaces");
      }
    }
  })


    // عرض النص في رسالة Frappe
    // frappe.msgprint({
    //     message: transcript,
    //     title: "النص المحول",
    //     indicator: "green"
    // });
};

// التعرف على الأخطاء في التعرف على الصوت
recognition.onerror = function(event) {
    console.error('حدث خطأ في التعرف على الصوت: ', event.error);
    frappe.msgprint({
        message: 'حدث خطأ في التعرف على الصوت',
        title: "خطأ",
        indicator: "red"
    });
};

// بدء التعرف على الصوت عند الضغط على الزر مثلاً
// document.getElementById('startRecordingButton').addEventListener('click', function() {
    recognition.start();
// });

}
}
});