import { marked } from 'marked'

/**
 * Normalizes mathematical formulas and LaTeX expressions into clean, legible plain text / code notation.
 */
export function cleanLatexMath(raw: string): string {
  if (!raw) return ''
  let res = raw

  // 1. Unwrap \text{...} wrappers: \text{TP} -> TP
  res = res.replace(/\\text\{([^{}]+)\}/g, '$1')

  // 2. Resolve \frac{numerator}{denominator} into (numerator / denominator)
  for (let i = 0; i < 5; i++) {
    if (!/\\frac\{([^{}]+)\}\{([^{}]+)\}/.test(res)) break
    res = res.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '($1 / $2)')
  }

  // 3. Convert LaTeX arithmetic & logical operators into standard Unicode symbols
  res = res.replace(/\\times/g, '×')
           .replace(/\\div/g, '÷')
           .replace(/\\approx/g, '≈')
           .replace(/\\cdot/g, '·')
           .replace(/\\pm/g, '±')
           .replace(/\\leq?/g, '≤')
           .replace(/\\geq?/g, '≥')
           .replace(/\\neq/g, '≠')
           .replace(/\\rightarrow/g, '→')
           .replace(/\\leftarrow/g, '←')

  // 4. Transform block math ($$ ... $$) into clean monospace expressions
  res = res.replace(/\$\$([\s\S]+?)\$\$/g, (_, formula) => {
    return '`' + formula.trim() + '`'
  })

  // 5. Transform inline math ($ ... $) into inline code expressions
  res = res.replace(/\$([^$\n]+)\$/g, (_, formula) => {
    return '`' + formula.trim() + '`'
  })

  // 6. Format bracket citations like [S1], [S2] into neat inline chips if they are standalone
  res = res.replace(/\[(S\d+)\](?!\()/g, '<span class="inline-citation">$1</span>')

  return res
}

/**
 * Parses markdown into safe, beautifully formatted HTML with GitHub-flavored markdown and responsive tables.
 */
export function renderMarkdownToHtml(markdownText: string): string {
  if (!markdownText) return ''
  const preprocessed = cleanLatexMath(markdownText)
  
  let html = marked.parse(preprocessed, {
    gfm: true,
    breaks: true,
  }) as string

  // Wrap any generated <table> in a responsive scroll container
  html = html
    .replace(/<table>/g, '<div class="table-container"><table>')
    .replace(/<\/table>/g, '</table></div>')

  return html
}

