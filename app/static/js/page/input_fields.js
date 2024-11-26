(function () {
  "use strict";
  var jQueryPlugin = (window.jQueryPlugin = function (ident, func) {
    return function (arg) {
      if (this.length > 1) {
        this.each(function () {
          var $this = $(this);

          if (!$this.data(ident)) {
            $this.data(ident, func($this, arg));
          }
        });

        return this;
      } else if (this.length === 1) {
        if (!this.data(ident)) {
          this.data(ident, func(this, arg));
        }

        return this.data(ident);
      }
    };
  });
})();

(function () {
  "use strict";
  function Pass_Show_Hide($root) {
    const element = $root;
    const pass_target = $root.first("data-password");
    const pass_elemet = $root.find("[data-pass-target]");
    const pass_show_hide_btn = $root.find("[data-pass-show-hide]");
    const pass_show = $root.find("[data-pass-show]");
    const pass_hide = $root.find("[data-pass-hide]");
    $(pass_hide).hide();
    $(pass_show_hide_btn).click(function () {
      if (pass_elemet.attr("type") === "password") {
        pass_elemet.attr("type", "text");
        $(pass_show).hide();
        $(pass_hide).show();
      } else {
        pass_elemet.attr("type", "password");
        $(pass_hide).hide();
        $(pass_show).show();
      }
    });
  }
  $.fn.Pass_Show_Hide = jQueryPlugin("Pass_Show_Hide", Pass_Show_Hide);
  $("[data-password]").Pass_Show_Hide();
})();
