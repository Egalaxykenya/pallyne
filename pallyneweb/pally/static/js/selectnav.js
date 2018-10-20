/**
 * @preserve SelectNav.js (v. 0.1)
 * Converts your <ul>/<ol> navigation into a dropdown list for small screens
 * https://github.com/lukaszfiszer/selectnav.js
 * Licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 */

window.selectnav = (function() {
	
	"use strict";
	
	var selectnav = function(element,options) {
		
		element = document.getElementById(element);
		
		// return immediately if element doesn't exist
		if (!element) {
			return;
		}
		
		// return immediately if element is not a list
		if (!islist(element)) {
			return;
		}
		
		// retreive options and set defaults
		var o = options || {},
			activeclass = o.activeclass || 'active',
			autoselect = typeof(o.autoselect) === "boolean" ? o.autoselect : true,
			nested = typeof(o.nested) === "boolean" ? o.nested : true,
			indent = o.indent || "→",
			label = o.label || "- Navigation -",
			
			// helper variables
			level = 0,
			selected = " selected ";
		
		// insert the freshly created dropdown navigation after the existing navigation
		element.insertAdjacentHTML('afterend', parselist(element) );
		
		var nav = document.getElementById(id());
		
		// autoforward on click
		if (nav.addEventListener) {
			nav.addEventListener('change', goTo);
		}
		if (nav.attachEvent) {
			nav.attachEvent('onchange', goTo);
		}
		
		return nav;
		
		function goTo(e){
		
			// Crossbrowser issues - http://www.quirksmode.org/js/events_properties.html
			var targ;
			if (!e) e = window.event;
			if (e.target) targ = e.target;
			else if (e.srcElement) targ = e.srcElement;
			if (targ.nodeType === 3) // defeat Safari bug
			targ = targ.parentNode; 
			
			if (targ.value) window.location.href = targ.value; 
		}
		
		function islist(list) {
			var n = list.nodeName.toLowerCase();
			return (n === 'ul' || n === 'ol');
		}
		
		function isMegaMenu(list) {
			var n = list.className.toLowerCase();
			return (n === 'sf-mega');
		}
		
		function id(nextId) {
			for (var j=1; document.getElementById('selectnav'+j); j++) {};
			return (nextId) ? 'selectnav'+j : 'selectnav'+(j-1);
		}
		
		function parselist(list, depth) {
			
			// go one level down
			level++;
			
			var length = list.children.length,
				html = '',
				prefix = '',
				k = level-1;
			
			// return immediately if has no children
			if (!length) {
				return;
			}
			
			if (depth) { k = depth-1; }
			
			if (k) {
				while(k--) {
					prefix += indent;
				}
				prefix += " ";
			}
			
			for (var i=0; i < length; i++) {
				
				var link = list.children[i].children[0];
				
				if (typeof(link) !== 'undefined') {
					var text = link.innerText || link.textContent;
					var isselected = '';
					
					if (activeclass) {
						isselected = link.className.search(activeclass) !== -1 || link.parentElement.className.search(activeclass) !== -1 ? selected : '';
					}
					if (autoselect && !isselected) {
						isselected = link.href === document.URL ? selected : '';
					}
					
					html += '<option value="' + link.href + '" ' + isselected + '>' + prefix + text +'</option>';
					
					if (nested) {
						var subElement = list.children[i].children[1];
						if (subElement && islist(subElement)) {
							html += parselist(subElement);
						} else if (subElement && isMegaMenu(subElement)) {
							var sectionNum = subElement.children[0].children.length;
							
							for (var j=0; j < sectionNum; j++) {
								var header = subElement.children[0].children[j].children[0],
									sectionList = subElement.children[0].children[j].children[1],
									headerNodeName = header.nodeName.toLowerCase(),
									headerLabelPrefix = indent + " ";
								
								if (header && (headerNodeName === 'h3' || headerNodeName === 'h4' || headerNodeName === 'h5')) {
									var headerLabel = header.innerText || header.textContent;
									if (headerLabel) {
										html += '<option value="" disabled>' + headerLabelPrefix + headerLabel +'</option>';
									}
								}
								if (sectionList && islist(sectionList)) {
									html += parselist(sectionList, 3);
								}
							}
							
						}
					}
				}
			}
			
			// adds label
			if (level === 1 && label) {
				html = '<option value="">' + label + '</option>' + html;
			}
			
			// add <select> tag to the top level of the list
			if (level === 1) {
				html = '<select class="selectnav" id="'+id(true)+'">' + html + '</select>';
			}
			
			// go 1 level up
			level--;
			
			return html;
		}
		
	};

	return function (element,options) {
		selectnav(element,options);
	};


})();
