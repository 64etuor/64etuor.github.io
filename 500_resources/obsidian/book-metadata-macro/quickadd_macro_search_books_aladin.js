const notice = (msg) => new Notice(msg, 5000);

const parseDOMFormString = (html) => {
  return new DOMParser().parseFromString(html, "text/html");
};

const requestHtmlDoc = async (url) => {
  const response = await request({ url });
  return parseDOMFormString(response);
};

const searchBooks = async (keyword) => {
  try {
    const doc = await requestHtmlDoc(
      "https://www.aladin.co.kr/m/msearch.aspx?SearchTarget=All&SearchWord=" +
        encodeURI(keyword)
    );
    return Array.from(
      doc.querySelectorAll("#Search3_Result .browse_list_box tr")
    )
      .map((e) => {
        const title = e.querySelector(".b_book_t")?.innerText.trim();
        if (!/도서|eBook|외서/i.test(title)) {
          return null;
        }
        const link = e.querySelector("a")?.href;
        const preview = e.querySelector(".btn_large a")?.href;
        const authors = e
          .querySelector(".b_list2 li:nth-of-type(2)")
          ?.innerText.trim()
          .replace(/\s?(\(|,)\s?/g, "$1");
        const publisher = e
          .querySelector(".b_list2 li:nth-of-type(3) a.nm_book_title_a")
          ?.innerText.trim();
        const publishedDate = e
          .querySelector(".b_list2 li:nth-of-type(3) span.nm_book_title_a")
          ?.innerText.trim();
        return {
          title,
          link,
          authors,
          publisher,
          publishedDate,
          preview,
        };
      })
      .filter((isNotNull) => isNotNull);
  } catch (err) {
    console.warn(err);
    notice(err.toString());
  }
  return [];
};

const getBookInfo = async (bookLink) => {
  try {
    const itemId = bookLink.split("ItemId=")?.[1];
    const infoLink = `https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=${itemId}`;
    const infoMobileLink = `https://www.aladin.co.kr/m/mproduct.aspx?ItemId=${itemId}`;

    // HTML 문서 가져오기
    const doc = await requestHtmlDoc(infoLink);

    // 메타데이터
    const metadata = JSON.parse(
      doc.querySelector('script[type="application/ld+json"]')?.innerText || "{}"
    );
    if (!metadata) {
      return null;
    }

    // 전체 페이지 수
    const totalPage =
      parseInt(
        /\d+쪽/.exec(doc.querySelector(".conts_info_list1")?.innerText)?.[0],
        10
      ) || 0;

    // 카테고리
    const categories = Array.from(
      doc.querySelectorAll("#ulCategory li:first-child a")
    )
      .map((e) => e.style.display !== "none" && e?.innerText.trim())
      .filter((val) => val && val !== "접기");

    // 저자
    const authors = metadata.author.name
      .split(",")
      .map((val) => val.replace(/\s(지음|옮김)/g, "").trim());

    // ISBN13
    const isbn = metadata.workExample?.[0].isbn;

    // 미리보기 링크
    const previewLink = `https://www.aladin.co.kr/shop/book/wletslookViewer.aspx?ISBN=${isbn}`;
    const previewMobileLink = `https://www.aladin.co.kr/m/mletslooks.aspx?ISBN=${isbn}#ItemCover`;

    console.log(metadata);

    return {
      title: metadata.name,
      image: metadata.image,
      publisher: metadata.publisher.name,
      publishedDate: metadata.workExample?.[0].datePublished,
      rating: metadata.aggregateRating?.ratingValue || 0,
      description: metadata.description,
      authors,
      categories,
      totalPage,
      infoLink,
      infoMobileLink,
      previewLink,
      previewMobileLink,
      isbn,
    };
  } catch (err) {
    console.warn(err);
    notice(err.toString());
  }
  return {};
};

const replaceIllegalFileNameCharactersInString = (str) => {
  return str
    .replace(/[\\,#%&\{\}\/*<>?$\'\":@\[\]\|\.]*/g, "")
    .replace(/\s{2,}/g, " ")
    .slice(0, 40);
};

module.exports = async function (plugin) {
  console.log("QuickAdd Macro Script Starting...");
  try {
    const query = await plugin.quickAddApi.inputPrompt(
      "제목, 저자, 출판사, ISBN 검색"
    );
    if (query) {
      const searchedBooks = await searchBooks(query);
      if (!searchedBooks) {
        return notice(`"${query}" was not found`);
      }

      const pickedBook = await plugin.quickAddApi.suggester(
        ({ title, authors, publisher, publishedDate }) =>
          `${title}\n${authors} | ${publisher} | ${publishedDate}`,
        searchedBooks
      );

      const book = await getBookInfo(pickedBook.link);
      if (book) {
        const fileName = replaceIllegalFileNameCharactersInString(book.title);
        plugin.variables = {
          ...book,
          fileName,
          author: book.authors[0],
          category: book.categories[1],
        };
      }
    }
  } catch (err) {
    console.warn(err);
    notice(err.toString());
  }
};