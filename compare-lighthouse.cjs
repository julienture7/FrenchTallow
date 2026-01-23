const fs = require('fs');
const mobile = JSON.parse(fs.readFileSync('lighthouse-report-v2.report.json', 'utf8'));
const desktop = JSON.parse(fs.readFileSync('lighthouse-desktop.report.json', 'utf8'));

console.log('=== MOBILE vs DESKTOP COMPARISON ===\n');

console.log('                    MOBILE    DESKTOP');
console.log('                    -------   -------');
console.log('Performance:         ' + mobile.categories.performance.score + '        ' + desktop.categories.performance.score);
console.log('Accessibility:       ' + mobile.categories.accessibility.score + '        ' + desktop.categories.accessibility.score);
console.log('Best Practices:      ' + mobile.categories['best-practices'].score + '        ' + desktop.categories['best-practices'].score);
console.log('SEO:                 ' + mobile.categories.seo.score + '        ' + desktop.categories.seo.score);
console.log('');

console.log('=== CORE WEB VITALS COMPARISON ===\n');
console.log('                    MOBILE      DESKTOP');
console.log('                    -------     -------');
console.log('FCP:                ' + mobile.audits['first-contentful-paint'].displayValue + '    ' + desktop.audits['first-contentful-paint'].displayValue);
console.log('LCP:                ' + mobile.audits['largest-contentful-paint'].displayValue + '    ' + desktop.audits['largest-contentful-paint'].displayValue);
console.log('TBT:                ' + mobile.audits['total-blocking-time'].displayValue + '     ' + desktop.audits['total-blocking-time'].displayValue);
console.log('CLS:                ' + mobile.audits['cumulative-layout-shift'].displayValue + '        ' + desktop.audits['cumulative-layout-shift'].displayValue);
console.log('Speed Index:        ' + mobile.audits['speed-index'].displayValue + '    ' + desktop.audits['speed-index'].displayValue);
console.log('');

// Check for issues
const mobileFailed = Object.keys(mobile.audits).filter(k => mobile.audits[k].score < 1 && mobile.audits[k].score !== null && mobile.audits[k].scoreDisplayMode !== 'notApplicable' && mobile.audits[k].scoreDisplayMode !== 'informative');
const desktopFailed = Object.keys(desktop.audits).filter(k => desktop.audits[k].score < 1 && desktop.audits[k].score !== null && desktop.audits[k].scoreDisplayMode !== 'notApplicable' && desktop.audits[k].scoreDisplayMode !== 'informative');

console.log('=== ISSUES ===');
console.log('Mobile issues:', mobileFailed.length);
console.log('Desktop issues:', desktopFailed.length);
