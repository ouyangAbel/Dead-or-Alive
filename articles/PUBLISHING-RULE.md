# DOA6 Last Round Site - Article Publishing Rule

## Project
D:\chuhaiWEB\Dead or Alive 6 Last Round

## Rule: Homepage Latest Articles Display

When publishing a new article on the DOA6 Last Round guide site:

1. Create the article in articles/ directory
2. Update articles.html (listing page) - add a new article card at the top
3. Update index.html - replace one "More Articles Coming Soon" placeholder in the #articles section with the new article card
4. Maximum 4 articles on homepage; if all 4 slots used, replace the oldest and move it to listing page only

## Key Files
- index.html: homepage, section id "articles" (class "latest-articles"), .la-grid has 4 card slots
- articles.html: listing page, shows ALL articles with no limit
- articles/: individual article HTML files

## Article Card Pattern (homepage)
<a href="articles/slug.html" class="la-card reveal">
  <div class="la-card-img"><img src="images/xxx.svg" alt="..." loading="lazy"></div>
  <div class="la-card-tag">CATEGORY</div>
  <h3>Title</h3>
  <p>Description.</p>
  <div class="la-card-meta"><span>Date</span><span>Read time</span></div>
</a>

## Placeholder Card Pattern (empty slots)
<a href="articles.html" class="la-card la-card-placeholder reveal">
  <div class="la-card-upcoming">
    <span class="la-card-plus">+</span>
    <h3>More Articles Coming Soon</h3>
    <p>Upcoming content description.</p>
  </div>
</a>

## Notes
- Navigation on all pages links to articles.html (listing page), not individual articles
- articles.html always shows all articles, no 4-item limit
