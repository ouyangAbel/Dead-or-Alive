# DOA6 Last Round Site - Article Publishing Rule

## Project
D:\chuhaiWEB\Dead or Alive 6 Last Round

## Rule: Homepage Latest Articles Display

When publishing a new article on the DOA6 Last Round guide site:

1. Create the article in articles/ directory
2. Update articles.html (listing page) - add a new article card at the top
3. Update index.html - add the new article card to the #articles .la-grid section
4. Maximum 20 articles on homepage; if all 20 slots used, remove the oldest to keep the grid at 20
5. No placeholder cards — only display actual articles; empty slots are not rendered

## Key Files
- index.html: homepage, section id "articles" (class "latest-articles"), .la-grid holds up to 20 cards
- articles.html: listing page, shows ALL articles with no limit
- articles/: individual article HTML files

## Article Card Pattern (homepage)
<a href="articles/slug.html" class="la-card reveal">
  <div class="la-card-tag">CATEGORY</div>
  <h3>Title</h3>
  <p>Description.</p>
  <span class="la-card-date">Date</span>
</a>

## Notes
- Navigation on all pages links to articles.html (listing page), not individual articles
- articles.html always shows all articles with no limit
- Homepage grid uses CSS: grid-template-columns: repeat(4, 1fr), responsive down to 1 column
- When homepage reaches 20 cards, rotate the oldest article off the homepage (it stays on articles.html)
