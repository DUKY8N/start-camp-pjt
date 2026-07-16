export function removeHtmlTags(value = '') {
  return String(value)
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]*>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

export function extractHomepageUrl(homepage = '') {
  const hrefMatch = String(homepage).match(/href=["']([^"']+)["']/i)

  if (hrefMatch) return hrefMatch[1]
  return removeHtmlTags(homepage)
}

export function normalizeHomepageUrl(homepage = '') {
  const value = extractHomepageUrl(homepage).trim()

  if (!value) return ''
  if (/^https?:\/\//i.test(value) || value.startsWith('//')) return value
  if (value.startsWith('/')) return value

  return `https://${value}`
}
