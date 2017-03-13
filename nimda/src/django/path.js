/*
 * Path v 1.2 2011-02-12
 *
 * Copyright (c) 2011, Aino
 * Licensed under the MIT license.
 */


var absUrl = function (url) {

  var l = window.location, h, p, f, i, n;

  if (/^\w+:/.test(url)) {
    return url.toString();
  }

  h = l.protocol + '//' + l.host;
  if (url.indexOf('/') === 0) {
    return h + url.toString();
  }

  p = l.pathname.replace(/\/[^\/]*$/, '');
  f = url.match(/\.\.\//g);

  if (f) {
    n = url.substring(f.length * 3);
    for (i = f.length; i--;) {
      p = p.substring(0, p.lastIndexOf('/'));
    }
  } else {
    n = url.toString();
  }
  return h + p + '/' + n;

},

  compareArray = function (o, t) {

    var i;

    if (o.length !== t.length) {
      return false;
    }

    for (i = 0; i < t.length; i++) {
      if (o[i] !== t[i]) {
        return false;
      }
    }
    return true;
  },

  trim = function (url) {
    return url.replace(/#.*$/, '').replace(/\?.*/, '').replace(/\/$/, '');
  },

  location = trim(window.location.href).split('/'),

  isAnchor = function (elem) {
    return !!(elem.href && elem.nodeName.toUpperCase() === 'A');
  },

  href = function (elem) {
    return trim(absUrl(elem.href)).split('/');
  };

$.extend($.expr[":"], {

  path: function (elem) {

    if (!isAnchor(elem)) {
      return false;
    }

    var anchor = href(elem);

    // if anchor points to root, activate if arrays are equal
    if (anchor.length === 3) {
      return compareArray(location, anchor);
    }

    return (location.length < anchor.length) ? false :
      compareArray(location.slice(0, anchor.length), anchor);

  },

  current: function (elem) {

    if (!isAnchor(elem)) {
      return false;
    }

    var anchor = href(elem);

    return compareArray(location, anchor);

  }
})