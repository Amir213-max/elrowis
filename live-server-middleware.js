/** Serve PDFs inline so the browser opens them instead of downloading. */
module.exports = function pdfInlineMiddleware(req, res, next) {
  if (/\.pdf(?:\?|$)/i.test(req.url)) {
    res.setHeader("Content-Type", "application/pdf");
    res.setHeader("Content-Disposition", "inline");
  }
  next();
};
