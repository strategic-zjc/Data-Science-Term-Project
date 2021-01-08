angular.module("formus").run(["$templateCache", function($templateCache) {$templateCache.put("formus/form.html","<form role=form id={{name}} class={{config.class}} style={{config.style}} ng-submit=submit()><header><div ng-if=\"config.showErrors && !isValid\" class=\"alert alert-danger\"><ul><li ng-repeat=\"e in errorList\" ng-bind=e></li></ul></div></header><formus-field config=fieldset class=special></formus-field><div class=clear-fix></div><footer><div ng-repeat=\"btn in config.buttons\" class=pull-left><button class={{btn.class}} type=button ng-if=!btn.items ng-click=callHandler(btn)>{{btn.title}}</button><div class=\"btn-group margin-left-5\" ng-if=btn.items><button class=\"{{btn.class}} dropdown-toggle\" type=button data-toggle=dropdown>{{btn.title}} <span class=caret></span></button><ul class=dropdown-menu><li ng-repeat=\"item in btn.items\"><a ng-click=callHandler(item)>{{item.title}}</a></li></ul></div></div><button ng-if=config.submit type=submit class={{config.submit.class}} ng-bind=config.submit.title></button></footer></form>");
$templateCache.put("formus/inputs/button.html","<button type=button class={{config.class}} ng-bind=config.title ng-click=config.handler()></button>");
$templateCache.put("formus/inputs/checkbox.html","<div class=checkbox><label><input type=checkbox ng-true-value={{config.trueValue}} ng-false-value={{config.falseValue}} ng-model=model name={{config.name}}>{{config.label}}</label></div>");
$templateCache.put("formus/inputs/checklist.html","<div ng-if=!config.inline><div class=checkbox ng-repeat=\"item in config.items\"><label><input ng-true-value={{config.trueValue}} ng-false-value={{config.falseValue}} name={{name}} type=checkbox ng-model=$parent.$parent.model[item.value]>{{item.title}}</label></div></div><div ng-if=config.inline><label class=checkbox-inline ng-repeat=\"item in config.items\"><input ng-true-value={{config.trueValue}} ng-false-value={{config.falseValue}} name={{name}} type=checkbox ng-model=$parent.$parent.model[item.value]>{{item.title}}</label></div>");
$templateCache.put("formus/inputs/fieldset.html","<div class={{config.class}}><formus-wrapper ng-repeat=\"field in config.fields\" class={{config.wrapClass}}><formus-field config=field></formus-field></formus-wrapper></div>");
$templateCache.put("formus/inputs/message.html","<div class=\"alert alert-{{config.type}} {{config.class}}\">{{model}}</div>");
$templateCache.put("formus/inputs/radio.html","<div ng-if=!config.inline><div class=radio ng-repeat=\"item in config.items\"><label><input ng-value=item.value name={{name}} type=radio ng-model=$parent.$parent.model>{{item.title}}</label></div></div><div ng-if=config.inline><label class=radio-inline ng-repeat=\"item in config.items\"><input ng-value=item.value name={{name}} type=radio ng-model=$parent.$parent.model>{{item.title}}</label></div>");
$templateCache.put("formus/inputs/select.html","<select name={{config.name}} ng-model=model class=form-control ng-multiple=config.multiple style={{config.style}} id={{config.name}} ng-options=\"item.value as item.title for item in config.items\"><option value ng-if=config.empty>{{config.empty}}</option></select>");
$templateCache.put("formus/inputs/textarea.html","<textarea ng-readonly=config.readonly class=form-control placeholder={{config.placeholder?config.placeholder:config.label}} rows={{config.rows}} ng-model=model name={{config.name}} id={{config.name}} style={{config.style}}>\n</textarea>");
$templateCache.put("formus/inputs/textbox.html","<div ng-class=\"{\'input-group\': config.addon}\"><div class=input-group-addon ng-if=config.addon ng-bind=config.addon></div><input ng-readonly=config.readonly ng-model=model class=form-control id={{config.name}} name={{config.name}} placeholder={{config.placeholder?config.placeholder:config.label}}></div>");
$templateCache.put("formus/inputs/wrapper.html","<div class=\"form-group margin-bottom-5\" ng-class=\"{\'has-error\': !input.isValid}\"><label for={{input.config.name}} ng-if=input.config.showLabel ng-bind=input.config.label></label><div ng-transclude=\"\"></div><span class=help-block ng-if=input.config.showErrors ng-repeat=\"e in input.errors\" ng-bind=e></span></div>");}]);