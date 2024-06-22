import requests
import re
import time

from scripts.pdfs.pdfs_to_images import download_pdfs

def find_pdf_strings(data):
    pdf_indices = [m.start() for m in re.finditer(r'\.pdf', data)]
    pdf_strings = []
    
    for index in pdf_indices:
        start_index = index
        while data[start_index] != '/':
            start_index -= 1
        pdf_strings.append(data[start_index:index+4])  # Including the ".pdf" extension

    return pdf_strings





def scrape_irs_page_for_paperwork_forms(page_size):
    url = "https://www.irs.gov/views/ajax?_wrapper_format=drupal_ajax&find=form&items_per_page=25&view_name=pup_picklists&view_display_id=forms_and_pubs&view_args=&view_path=%2Fnode%2F108781&view_base_path=&view_dom_id=b1031c585c3fcd41fee2954810be0a5de95428ce8c862df92365a48c977bff72&pager_element=0&_drupal_ajax=1&ajax_page_state%5Btheme%5D=pup_irs&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=accordion_menus%2Faccordion_menus_widget%2Caddtoany%2Faddtoany.front%2Cbetter_exposed_filters%2Fauto_submit%2Cbetter_exposed_filters%2Fgeneral%2Cbootstrap%2Fpopover%2Cbootstrap%2Ftooltip%2Cchosen%2Fdrupal.chosen%2Cchosen_lib%2Fchosen.css%2Cdatalayer%2Fbehaviors%2Cdownload_link_labeler%2Fdownload-link-labeler-theme%2Cextlink%2Fdrupal.extlink%2Cgoogle_tag%2Fgtag%2Cgoogle_tag%2Fgtag.ajax%2Cgoogle_tag%2Fgtm%2Clayout_discovery%2Fthreecol_25_50_25%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Cpup_base%2Fglobal-site-features%2Cpup_ckeditor_plugins%2Fpup_ckeditor_plugins%2Cpup_global_services%2Fpup_global_services%2Cpup_irs%2Fanalytics-scripts%2Cpup_irs%2Fglobal-scripts%2Cpup_irs%2Fglobal-site-features%2Cpup_irs%2Fglobal-styling%2Cpup_irs%2Fmatch-height%2Cpup_irs%2Fmega-menu%2Cpup_irs%2Fmenu-features%2Cpup_irs%2Fnon-front-print%2Cpup_irs%2Fsearch-features%2Cpup_simple_sitemap%2Fsimple_sitemap_overrides%2Cresponsive_tables_filter%2Ftablesaw-filter%2Csystem%2Fbase%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module"
    page_size = 25
    page = 62

    while True:
        headers = {
            "authority": "www.irs.gov",
            "method": "GET",
            "path": f"/views/ajax?_wrapper_format=drupal_ajax&find=form&items_per_page={page_size}&view_name=pup_picklists&view_display_id=forms_and_pubs&view_args=&view_path=%2Fnode%2F108781&view_base_path=&view_dom_id=b1031c585c3fcd41fee2954810be0a5de95428ce8c862df92365a48c977bff72&pager_element=0&_drupal_ajax=1&ajax_page_state%5Btheme%5D=pup_irs&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=accordion_menus%2Faccordion_menus_widget%2Caddtoany%2Faddtoany.front%2Cbetter_exposed_filters%2Fauto_submit%2Cbetter_exposed_filters%2Fgeneral%2Cbootstrap%2Fpopover%2Cbootstrap%2Ftooltip%2Cchosen%2Fdrupal.chosen%2Cchosen_lib%2Fchosen.css%2Cdatalayer%2Fbehaviors%2Cdownload_link_labeler%2Fdownload-link-labeler-theme%2Cextlink%2Fdrupal.extlink%2Cgoogle_tag%2Fgtag%2Cgoogle_tag%2Fgtag.ajax%2Cgoogle_tag%2Fgtm%2Clayout_discovery%2Fthreecol_25_50_25%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Cpup_base%2Fglobal-site-features%2Cpup_ckeditor_plugins%2Fpup_ckeditor_plugins%2Cpup_global_services%2Fpup_global_services%2Cpup_irs%2Fanalytics-scripts%2Cpup_irs%2Fglobal-scripts%2Cpup_irs%2Fglobal-site-features%2Cpup_irs%2Fglobal-styling%2Cpup_irs%2Fmatch-height%2Cpup_irs%2Fmega-menu%2Cpup_irs%2Fmenu-features%2Cpup_irs%2Fnon-front-print%2Cpup_irs%2Fsearch-features%2Cpup_simple_sitemap%2Fsimple_sitemap_overrides%2Cresponsive_tables_filter%2Ftablesaw-filter%2Csystem%2Fbase%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module",
            "scheme": "https",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": '_gid=GA1.2.928715639.1718725706; AKA_A2=A; _abck=8012A2907290B9CE19D58A329D214C56~-1~YAAQYvTVF7bMOfKPAQAAlenHLgzWqHSMWZNRpNg5g/GMZQ+Kmgc901MeX2sVDXYF3DHFs4zbSJDdO/p5cNuRJXjrG+A3PYOdY09eMd4JNc8QZchHcEsgDDZ8EYkUMg4MqOZ9S84ir7kz4oTxWO8XRV5BZk/vOpTEyUyC3cXqA1YI/TGmvip+6Ls9skvDbB2bqr9BkhnX19VEktmAXw9LR3DtU7MmGU2W4kf9NZ7JLpBfTSGVyiARucRlWSsO5WzRyyT1c8FVYbeCrFrQlSo0Z5I7Hgk82sqx37kdaHRgA4njXNaBEPId5ZKvt1i2HvXQz4XZ3JndvicZNnA0Y5/2huCnCGbLYKI75V8HsXuRNPVsBkVUHV305I9b/LglvVrkazqmznLBwQ==~-1~-1~-1; akaalb_DMAF_ALB_PROD=1718774724~op=~rv=55~m=~os=~id=60ac598cebc882837efac4a8595f03a5; bm_sz=9D6BF8C290BD465B6EA08E5E759ECCA6~YAAQYvTVF+k+OvKPAQAAtpD0LhjL0Js/q3cfXSyUP7/BILbYqibeAHjXoPqMO7JuoLg0b1Cjt0IJzVMlPvUtcsHGe5NWue43Xk+zZnLMGB0VpNbwKV58TEXap3MPSarGjvdo6Qa4+2BgsMcrL5pOK1stw7rYC5DTWUvTEhvrFAtlTn/kgjX5wD1RDqg4TSGLGM0lrGxKtfvN3yUVNSD+5IMj4QpsYZzMKZPDxVC/y/seicqEUAqR6D/2vWfBBgVj9FF+Ea6ulclmxlWw60Q5qNanamLNBrjp2YcLXvIPsy5ytbkxnEL62CMi8283qRYzqQzYn2Wdu/dxICufVxT3RydP8dyG84XwAlVyb7zlx2xIh/wCZLXn9cdxd4nl4xFxc9PnnggzchuEPfYIBnXCqL+yf5Wruhsqf2vnRq5AhI52A/AEsm1z6Q==~4536642~4408888; RT="z=1&dm=irs.gov&si=lu7m5djlbz&ss=lxkkwq0q&sl=0&tt=0"; _gat=1; _gat_GSA_ENOR0=1; _ga=GA1.1.1590870310.1718725706; _ga_CSLL4ZEK4L=GS1.1.1718771772.3.1.1718774698.0.0.0; _ga_ZY6FM95CS5=GS1.1.1718771772.3.1.1718774698.0.0.0; _gali=edit-find--3wpclPWKYxM',
            "Priority": "u=1, i",
            "Referer": "https://www.irs.gov/forms-instructions-and-publications",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "macOS",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }



        params = {
            "_wrapper_format": "drupal_ajax",
            "find": "form",
            "items_per_page": page_size,
            "view_name": "pup_picklists",
            "view_display_id": "forms_and_pubs",
            "view_args": "",
            "view_path": "/node/108781",
            "view_base_path": "",
            "view_dom_id": "b1031c585c3fcd41fee2954810be0a5de95428ce8c862df92365a48c977bff72",
            "pager_element": 0,
            "page": page,
            "_drupal_ajax": 1,
            "ajax_page_state[theme]": "pup_irs",
            "ajax_page_state[theme_token]": "",
            "ajax_page_state[libraries]": (
                "accordion_menus/accordion_menus_widget,"
                "addtoany/addtoany.front,"
                "better_exposed_filters/auto_submit,"
                "better_exposed_filters/general,"
                "bootstrap/popover,"
                "bootstrap/tooltip,"
                "chosen/drupal.chosen,"
                "chosen_lib/chosen.css,"
                "datalayer/behaviors,"
                "download_link_labeler/download-link-labeler-theme,"
                "extlink/drupal.extlink,"
                "google_tag/gtag,"
                "google_tag/gtag.ajax,"
                "google_tag/gtm,"
                "layout_discovery/threecol_25_50_25,"
                "paragraphs/drupal.paragraphs.unpublished,"
                "pup_base/global-site-features,"
                "pup_ckeditor_plugins/pup_ckeditor_plugins,"
                "pup_global_services/pup_global_services,"
                "pup_irs/analytics-scripts,"
                "pup_irs/global-scripts,"
                "pup_irs/global-site-features,"
                "pup_irs/global-styling,"
                "pup_irs/match-height,"
                "pup_irs/mega-menu,"
                "pup_irs/menu-features,"
                "pup_irs/non-front-print,"
                "pup_irs/search-features,"
                "pup_simple_sitemap/simple_sitemap_overrides,"
                "responsive_tables_filter/tablesaw-filter,"
                "system/base,"
                "views/views.ajax,"
                "views/views.module"
            ),
        }

        response = requests.get(url, headers=headers, params=params)
        pdf_urls = find_pdf_strings(response.text)
        if len(pdf_urls) == 0:
            break
        for i in range(len(pdf_urls)):
            pdf_urls[i] = f"https://www.irs.gov/pub/irs-pdf/{pdf_urls[i]}"
        download_pdfs(pdf_urls, "data/raw")
        time.sleep(10)
        print(f"Downloaded {len(pdf_urls)} pdfs on page {page}")
        page += 1

scrape_irs_page_for_paperwork_forms(25)
