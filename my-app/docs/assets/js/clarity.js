(function(){
  var PID = window.CLARITY_PROJECT_ID || '';
  if(!PID) return; // no-op if not configured
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", PID);
  // SPA page tagging for MkDocs
  document.addEventListener('DOMContentLoaded', function(){
    clarity('page');
  });
})();
