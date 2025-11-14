export function shortText(txt, n=300){
  if(!txt) return ''
  return txt.length > n ? txt.slice(0,n) + '...' : txt
}
