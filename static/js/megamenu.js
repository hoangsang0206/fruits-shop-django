const loadCategories = () => {
    $.ajax({
        url: 'api/loai/?format=json',
        type: 'GET',
        success: (response) => {
            $('.menu .megamenu, .hidden-menu .megamenu').empty();
            $('.mobile-sidebar .megamenu').empty();
            $('.sub-header-item-list').empty();

            let index = 0;
            response.map((item) => {
                const el = `<li class="megamenu-item">
                        <div class="megamenu-item-box">
                            <a href="/loai/${item.MaLoai}" class="megamenu-link">
                                ${item.TenLoai}
                            </a>
                            <i class="fa-solid fa-chevron-right megamenu-chevron"></i>
                        </div>
                    </li>`;

                var _el = `<li class="sub-header-item">
                    <a href="/loai/${item.MaLoai}" class="sub-header-link">${item.TenLoai}</a>
                </li>`;
                                    
                if(index < 14) {
                    
                    $('.menu .megamenu, .hidden-menu .megamenu').append(el);
                }
                $('.mobile-sidebar .megamenu').append(el);
                $('.sub-header-item-list').append(_el);

                index += 1;
            })
        },
        error: (error) => {
            console.error('Cannot get categories')
        }
    })
}

loadCategories()