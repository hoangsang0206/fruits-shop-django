﻿//Show/hide web loader
function showWebLoader() {
    $('.webloading').css('display', 'grid');
}

function hideWebLoader() {
    $('.webloading').hide();
}


//Update quantity of item in cart to header
function updateCartCount() {
    $.ajax({
        type: 'GET',
        url: '/api/giohang/capnhat',
        success: (data) => {
            $('.cart-count').html(data.tong);
        },
        error: () => {
            $('.cart-count').html(0);
        }
    })
}

$(document).ready(() => {
    updateCartCount();
})

//-Add product to cart ------------------------------------
$('.add-to-cart-btn, .buy-action-btn').click(function() {
    const productID = $(this).data('product-id');

    if (productID.length > 0) {
        showWebLoader();
        $.ajax({
            type: 'POST',
            url: '/api/giohang/them',
            data: {
                id: productID,
                csrfmiddlewaretoken: $('#csrf_token_input').val()
            },
            success: (respone) => {
                setTimeout(hideWebLoader, 500);
                updateCartCount();
            }
        })
    }   
})

$('.buy-action-btn').click(() => {
    setTimeout(() => { window.location.href = '/giohang' }, 510)
})

$('.btn-add-to-cart').click(function() {
    const productID = $(this).data('product');
    
    if (productID.length > 0) {
        $.ajax({
            type: 'POST',
            url: '/api/giohang/them',
            data: {
                id: productID,
                csrfmiddlewaretoken: $('#csrf_token_input').val()
            },
            success: (respone) => {
                updateCartCount();
            }
        })
    }
})

//-------------------------------
$('.not-logged-in').click(() => {
    window.location.href = '/dangnhap'
})

//---------------------------------
$(document).ready(() => {
    const cartFormInput = $('.cart-form input').toArray();
    cartFormInput.forEach((input) => {
        checkInputValid($(input));
    })

    if ($('#cod-method').is(':checked')) {
        $('.input-ship-info').show();
    }

    $('input[name="shipmethod"]').on('change', () => {
        if ($('#cod-method').is(':checked')) {
            $('.input-ship-info').show();
        }
        else {
            $('.input-ship-info').hide();
        }
    })
})

//---------------------------------
function activeCartStep(step1, step2, step3, step4) {
    $(step1).addClass('step-active');
    $(step2).addClass('step-active');
    $(step3).addClass('step-active');
    $(step4).addClass('step-active');
}

function disAciveStep(step2, step3, step4) {
    $(step2).removeClass('step-active');
    $(step3).removeClass('step-active');
    $(step4).removeClass('step-active');
}

function showCartInfo() {
    var idFromUrl = window.location.hash.substring(1);
    if (idFromUrl.length > 0) {
        hideCartInfo();
        $('#' + idFromUrl).addClass('form-current');

        disAciveStep('.step-2', '.step-3', '.step-4');

        if (idFromUrl == 'cart-order-box') {
            activeCartStep('.step-1', '.step-2');
        }
    }
}

function hideCartInfo() {
    var cartInfoList = $('.cart-info').toArray();
    cartInfoList.forEach((item) => {
        $(item).removeClass('form-current');
    })
}

$(document).ready(() => {
    showCartInfo();

    $(window).on('hashchange', () => {
        showCartInfo();
    })
})

//--Update cart item quantity
$('.update-quantity').click(function() {
    const productID = $(this).data('product-btn');
    const updateType = $(this).data('update');
    const inputQuantity = $(this).parent('.cart-product-quantity').children('input[name="quantity"]');

    if (productID.length > 0 && updateType.length > 0) {
        showWebLoader();
        $.ajax({
            type: 'PUT',
            url: '/api/giohang/capnhatsoluong',
            headers: { "X-CSRFToken": $('#csrf_token_input').val() },
            data: {
                id: productID,
                type: updateType
            },
            success: (res) => {
                setTimeout(hideWebLoader, 500);
                inputQuantity.val(res.qty);

                var total = res.total.toLocaleString("vi-VN") + 'đ';
                $('.total-price').empty();
                $('.total-price').text(total);
            },
            error: () => { hideWebLoader(); }
        })
    }
})

//--------
$('input[name="quantity"]').focus((e) => {
    var currentVal = $(e.target).val();

    $(e.target).blur(() => {
        var newVal = $(e.target).val();
        var productID = $(e.target).data('product');
        if (newVal != currentVal) {
            showWebLoader();    
            $.ajax({
                type: 'PUT',
                url: '/api/giohang/capnhatsoluong',
                headers: { "X-CSRFToken": $('#csrf_token_input').val() },
                data: {
                    id: productID,
                    qty: newVal
                },
                success: (res) => {
                    setTimeout(hideWebLoader, 500);
                    $(e.target).val(res.qty);

                    var total = res.total.toLocaleString("vi-VN") + 'đ';
                    $('.total-price').empty();
                    $('.total-price').text(total);
                },
                error: () => { hideWebLoader(); }
            })
        }
    })
})


//-- Delete cart item
$('.delete-cart-item').click(function() {
    const productID = $(this).data('product');
    if (productID.length > 0) {
        $.ajax({
            type: 'DELETE',
            url: '/api/giohang/xoa',
            headers: { "X-CSRFToken": $('#csrf_token_input').val() },
            data: {
                id: productID
            },
            success: (respone) => {
                updateCartCount();
                window.location.href ='/giohang'
            }
        })
    }
})