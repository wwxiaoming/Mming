(function () {
  'use strict';

  var app = document.getElementById('app');
  var badge = document.getElementById('cart-badge');
  var toast = document.getElementById('toast');
  var toastTimer = null;
  var cartPageHandler = null;

  function showToast(message) {
    if (toastTimer) clearTimeout(toastTimer);
    toast.textContent = message;
    toast.classList.add('toast--visible');
    toastTimer = setTimeout(function () {
      toast.classList.remove('toast--visible');
    }, 2000);
  }

  function updateBadge() {
    var count = Cart.getTotalCount();
    badge.textContent = count;
    if (count > 0) {
      badge.classList.add('bump');
      setTimeout(function () { badge.classList.remove('bump'); }, 300);
    }
  }

  function formatPrice(price) {
    return '¥' + price.toLocaleString('zh-CN');
  }

  function getProductById(id) {
    for (var i = 0; i < products.length; i++) {
      if (products[i].id === id) return products[i];
    }
    return null;
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function renderHome() {
    var html = '<h2 class="page-title">精品系列</h2>';
    html += '<p class="page-subtitle">每一款，都是匠心之作</p>';
    html += '<div class="product-grid">';

    products.forEach(function (product) {
      html += '<div class="product-card" data-nav="product/' + product.id + '">';
      html += '<img class="product-card__image" src="' + product.image + '" alt="' + escapeHtml(product.name) + '" loading="lazy">';
      html += '<div class="product-card__body">';
      html += '<h3 class="product-card__name">' + escapeHtml(product.name) + '</h3>';
      html += '<p class="product-card__price">' + formatPrice(product.price) + '</p>';
      html += '<button class="product-card__btn" data-action="add-to-cart" data-id="' + product.id + '">加入购物车</button>';
      html += '</div></div>';
    });

    html += '</div>';
    app.innerHTML = html;

    var container = app.querySelector('.product-grid');
    container.classList.add('page-enter');

    container.addEventListener('click', function (e) {
      var card = e.target.closest('.product-card');
      var btn = e.target.closest('[data-action="add-to-cart"]');

      if (btn) {
        e.stopPropagation();
        var id = btn.getAttribute('data-id');
        var product = getProductById(id);
        if (product) {
          Cart.addItem(product);
          showToast('已添加到购物车');
        }
      } else if (card) {
        var nav = card.getAttribute('data-nav');
        if (nav) {
          window.location.hash = nav;
        }
      }
    });
  }

  function renderProduct(id) {
    var product = getProductById(id);
    if (!product) {
      renderNotFound();
      return;
    }

    var html = '';
    html += '<a class="btn-back" href="#home">';
    html += '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>';
    html += '返回首页</a>';

    html += '<div class="product-detail">';
    html += '<img class="product-detail__image" src="' + product.image + '" alt="' + escapeHtml(product.name) + '">';
    html += '<div class="product-detail__info">';
    html += '<h2 class="product-detail__name">' + escapeHtml(product.name) + '</h2>';
    html += '<p class="product-detail__price">' + formatPrice(product.price) + '</p>';
    html += '<p class="product-detail__desc">' + escapeHtml(product.description) + '</p>';
    html += '<div class="product-detail__actions">';
    html += '<div class="quantity-control">';
    html += '<button class="quantity-control__btn" data-action="qty-minus" ' + (1 <= 1 ? 'disabled' : '') + '>-</button>';
    html += '<input class="quantity-control__value" type="number" value="1" min="1" max="99" data-action="qty-input" readonly>';
    html += '<button class="quantity-control__btn" data-action="qty-plus">+</button>';
    html += '</div>';
    html += '<button class="btn-primary" data-action="detail-add-to-cart">加入购物车</button>';
    html += '</div></div></div>';

    app.innerHTML = html;

    var container = app.querySelector('.product-detail');
    container.classList.add('page-enter');

    var qtyInput = app.querySelector('[data-action="qty-input"]');
    var minusBtn = app.querySelector('[data-action="qty-minus"]');
    var plusBtn = app.querySelector('[data-action="qty-plus"]');

    function updateMinusBtn() {
      var val = parseInt(qtyInput.value) || 1;
      minusBtn.disabled = val <= 1;
    }

    minusBtn.addEventListener('click', function () {
      var val = parseInt(qtyInput.value) || 1;
      if (val > 1) {
        qtyInput.value = val - 1;
        updateMinusBtn();
      }
    });

    plusBtn.addEventListener('click', function () {
      var val = parseInt(qtyInput.value) || 1;
      if (val < 99) {
        qtyInput.value = val + 1;
        updateMinusBtn();
      }
    });

    app.querySelector('[data-action="detail-add-to-cart"]').addEventListener('click', function () {
      var qty = parseInt(qtyInput.value) || 1;
      Cart.addItem(product, qty);
      showToast('已添加到购物车');
    });
  }

  function renderCart() {
    var items = Cart.getItems();

    if (items.length === 0) {
      var html = '<div class="cart-empty page-enter">';
      html += '<div class="cart-empty__icon">';
      html += '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>';
      html += '</div>';
      html += '<h3 class="cart-empty__title">购物车是空的</h3>';
      html += '<p class="cart-empty__text">快去挑选心仪的包包吧</p>';
      html += '<a class="btn-primary" href="#home">去逛逛</a>';
      html += '</div>';
      app.innerHTML = html;
      return;
    }

    var html = '<h2 class="page-title">购物车</h2>';
    html += '<div class="cart-list">';

    items.forEach(function (item) {
      html += '<div class="cart-item">';
      html += '<img class="cart-item__image" src="' + item.product.image + '" alt="' + escapeHtml(item.product.name) + '" loading="lazy">';
      html += '<div class="cart-item__info">';
      html += '<h3 class="cart-item__name">' + escapeHtml(item.product.name) + '</h3>';
      html += '<p class="cart-item__price">' + formatPrice(item.product.price) + '</p>';
      html += '</div>';
      html += '<div class="cart-item__actions">';
      html += '<div class="quantity-control">';
      html += '<button class="quantity-control__btn" data-action="cart-minus" data-id="' + item.product.id + '" ' + (item.quantity <= 1 ? 'disabled' : '') + '>-</button>';
      html += '<span class="quantity-control__value" style="display:flex;align-items:center;justify-content:center;">' + item.quantity + '</span>';
      html += '<button class="quantity-control__btn" data-action="cart-plus" data-id="' + item.product.id + '">+</button>';
      html += '</div>';
      html += '<button class="cart-item__remove" data-action="cart-remove" data-id="' + item.product.id + '">删除</button>';
      html += '</div>';
      html += '</div>';
    });

    html += '</div>';

    html += '<div class="cart-summary">';
    html += '<div class="cart-summary__row">';
    html += '<span>商品总数</span>';
    html += '<span>' + Cart.getTotalCount() + ' 件</span>';
    html += '</div>';
    html += '<div class="cart-summary__row cart-summary__row--total">';
    html += '<span>合计</span>';
    html += '<span class="cart-summary__value">' + formatPrice(Cart.getTotalPrice()) + '</span>';
    html += '</div>';
    html += '<div class="cart-summary__actions">';
    html += '<a class="btn-outline" href="#home">继续购物</a>';
    html += '<a class="btn-primary" href="#checkout">去结算</a>';
    html += '</div>';
    html += '</div>';

    app.innerHTML = html;
    app.querySelector('.cart-list').classList.add('page-enter');

    var cartClickHandler = function (e) {
      var target = e.target.closest('[data-action]');
      if (!target) return;
      var action = target.getAttribute('data-action');
      var id = target.getAttribute('data-id');

      if (action === 'cart-minus') {
        var item = findCartItem(id);
        if (item && item.quantity > 1) {
          Cart.updateQuantity(id, item.quantity - 1);
          renderCart();
        }
      } else if (action === 'cart-plus') {
        var item2 = findCartItem(id);
        if (item2) {
          Cart.updateQuantity(id, item2.quantity + 1);
          renderCart();
        }
      } else if (action === 'cart-remove') {
        Cart.removeItem(id);
        renderCart();
      }
    };

    if (cartPageHandler) {
      app.removeEventListener('click', cartPageHandler);
    }
    cartPageHandler = cartClickHandler;
    app.addEventListener('click', cartClickHandler);
  }

  function findCartItem(productId) {
    var items = Cart.getItems();
    for (var i = 0; i < items.length; i++) {
      if (items[i].product.id === productId) return items[i];
    }
    return null;
  }

  function renderCheckout() {
    var items = Cart.getItems();

    if (items.length === 0) {
      window.location.hash = 'cart';
      return;
    }

    var html = '<h2 class="page-title">结算</h2>';
    html += '<div class="checkout">';

    html += '<div class="checkout__section">';
    html += '<h3 class="checkout__section-title">订单摘要</h3>';
    items.forEach(function (item) {
      html += '<div class="checkout-item">';
      html += '<span class="checkout-item__name">' + escapeHtml(item.product.name) + '</span>';
      html += '<span class="checkout-item__qty">x' + item.quantity + '</span>';
      html += '<span class="checkout-item__price">' + formatPrice(item.product.price * item.quantity) + '</span>';
      html += '</div>';
    });
    html += '<div class="checkout-total">';
    html += '<span>合计</span>';
    html += '<span class="checkout-total__value">' + formatPrice(Cart.getTotalPrice()) + '</span>';
    html += '</div>';
    html += '</div>';

    html += '<div class="checkout__section">';
    html += '<h3 class="checkout__section-title">收货信息</h3>';
    html += '<form id="checkout-form" novalidate>';
    html += '<div class="form-group">';
    html += '<label class="form-group__label">姓名 <span class="required">*</span></label>';
    html += '<input class="form-group__input" type="text" name="name" placeholder="请输入收货人姓名" autocomplete="name">';
    html += '<p class="form-group__error" data-error="name"></p>';
    html += '</div>';
    html += '<div class="form-group">';
    html += '<label class="form-group__label">手机号 <span class="required">*</span></label>';
    html += '<input class="form-group__input" type="tel" name="phone" placeholder="请输入11位手机号" autocomplete="tel">';
    html += '<p class="form-group__error" data-error="phone"></p>';
    html += '</div>';
    html += '<div class="form-group">';
    html += '<label class="form-group__label">收货地址 <span class="required">*</span></label>';
    html += '<input class="form-group__input" type="text" name="address" placeholder="请输入详细收货地址" autocomplete="street-address">';
    html += '<p class="form-group__error" data-error="address"></p>';
    html += '</div>';
    html += '<button type="submit" class="btn-submit">提交订单</button>';
    html += '</form>';
    html += '</div>';

    html += '</div>';

    app.innerHTML = html;
    app.querySelector('.checkout').classList.add('page-enter');

    var form = document.getElementById('checkout-form');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var nameInput = form.elements['name'];
      var phoneInput = form.elements['phone'];
      var addressInput = form.elements['address'];

      var valid = true;

      var nameErr = form.querySelector('[data-error="name"]');
      var phoneErr = form.querySelector('[data-error="phone"]');
      var addressErr = form.querySelector('[data-error="address"]');

      [nameInput, phoneInput, addressInput].forEach(function (inp) {
        inp.classList.remove('form-group__input--error');
      });
      [nameErr, phoneErr, addressErr].forEach(function (err) {
        err.classList.remove('form-group__error--visible');
      });

      var name = nameInput.value.trim();
      if (!name) {
        nameErr.textContent = '请输入收货人姓名';
        nameErr.classList.add('form-group__error--visible');
        nameInput.classList.add('form-group__input--error');
        valid = false;
      } else if (name.length < 2) {
        nameErr.textContent = '姓名至少需要2个字符';
        nameErr.classList.add('form-group__error--visible');
        nameInput.classList.add('form-group__input--error');
        valid = false;
      }

      var phone = phoneInput.value.trim();
      if (!phone) {
        phoneErr.textContent = '请输入手机号';
        phoneErr.classList.add('form-group__error--visible');
        phoneInput.classList.add('form-group__input--error');
        valid = false;
      } else if (!/^1\d{10}$/.test(phone)) {
        phoneErr.textContent = '请输入正确的11位手机号（以1开头）';
        phoneErr.classList.add('form-group__error--visible');
        phoneInput.classList.add('form-group__input--error');
        valid = false;
      }

      var address = addressInput.value.trim();
      if (!address) {
        addressErr.textContent = '请输入收货地址';
        addressErr.classList.add('form-group__error--visible');
        addressInput.classList.add('form-group__input--error');
        valid = false;
      } else if (address.length < 5) {
        addressErr.textContent = '收货地址至少需要5个字符';
        addressErr.classList.add('form-group__error--visible');
        addressInput.classList.add('form-group__input--error');
        valid = false;
      }

      if (valid) {
        var orderNumber = 'BS' + Date.now().toString(36).toUpperCase() + Math.random().toString(36).substring(2, 6).toUpperCase();
        window.location.hash = 'order-success/' + orderNumber;
      }
    });
  }

  function renderOrderSuccess(orderNumber) {
    var html = '<div class="order-success page-enter">';
    html += '<div class="order-success__icon">';
    html += '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="16 10 11 15 8 12"/></svg>';
    html += '</div>';
    html += '<h2 class="order-success__title">下单成功！</h2>';
    html += '<p class="order-success__text">感谢您的购买，我们会尽快为您安排发货</p>';
    html += '<p class="order-success__number">订单编号：' + orderNumber + '</p>';
    html += '<a class="btn-primary" href="#home">返回首页</a>';
    html += '</div>';

    app.innerHTML = html;

    Cart.clear();
  }

  function renderNotFound() {
    app.innerHTML = '<div class="cart-empty page-enter"><h3 class="cart-empty__title">页面未找到</h3><p class="cart-empty__text">您访问的页面不存在</p><a class="btn-primary" href="#home">返回首页</a></div>';
  }

  function route() {
    var hash = window.location.hash.replace('#', '') || 'home';

    if (hash === 'home' || hash === '') {
      renderHome();
    } else if (hash === 'cart') {
      renderCart();
    } else if (hash === 'checkout') {
      renderCheckout();
    } else if (hash.indexOf('product/') === 0) {
      var productId = hash.replace('product/', '');
      renderProduct(productId);
    } else if (hash.indexOf('order-success/') === 0) {
      var orderNumber = hash.replace('order-success/', '');
      renderOrderSuccess(orderNumber);
    } else {
      renderNotFound();
    }
  }

  function init() {
    updateBadge();

    Cart.onChange(function () {
      updateBadge();
    });

    window.addEventListener('hashchange', route);

    route();
  }

  window.App = {
    init: init
  };

  document.addEventListener('DOMContentLoaded', init);
})();