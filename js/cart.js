(function () {
  'use strict';

  var STORAGE_KEY = 'bellesac_cart';
  var listeners = [];

  function load() {
    try {
      var data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  }

  function save(items) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    } catch (e) {}
  }

  function notify() {
    listeners.forEach(function (fn) {
      try { fn(); } catch (e) {}
    });
  }

  function getItems() {
    return load();
  }

  function addItem(product, quantity) {
    var items = load();
    var qty = quantity || 1;
    var found = false;

    for (var i = 0; i < items.length; i++) {
      if (items[i].product.id === product.id) {
        items[i].quantity += qty;
        found = true;
        break;
      }
    }

    if (!found) {
      items.push({ product: product, quantity: qty });
    }

    save(items);
    notify();
  }

  function removeItem(productId) {
    var items = load();
    items = items.filter(function (item) {
      return item.product.id !== productId;
    });
    save(items);
    notify();
  }

  function updateQuantity(productId, quantity) {
    var items = load();
    if (quantity <= 0) {
      items = items.filter(function (item) {
        return item.product.id !== productId;
      });
    } else {
      for (var i = 0; i < items.length; i++) {
        if (items[i].product.id === productId) {
          items[i].quantity = quantity;
          break;
        }
      }
    }
    save(items);
    notify();
  }

  function getTotalPrice() {
    return load().reduce(function (total, item) {
      return total + item.product.price * item.quantity;
    }, 0);
  }

  function getTotalCount() {
    return load().reduce(function (total, item) {
      return total + item.quantity;
    }, 0);
  }

  function clear() {
    save([]);
    notify();
  }

  function onChange(callback) {
    listeners.push(callback);
  }

  window.Cart = {
    getItems: getItems,
    addItem: addItem,
    removeItem: removeItem,
    updateQuantity: updateQuantity,
    getTotalPrice: getTotalPrice,
    getTotalCount: getTotalCount,
    clear: clear,
    onChange: onChange
  };
})();