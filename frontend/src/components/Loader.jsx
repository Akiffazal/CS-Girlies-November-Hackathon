import React from 'react'
export default function Loader({size=20}){
  return (
    <div style={{display:'inline-block'}}>
      <svg width={size} height={size} viewBox="0 0 50 50">
        <circle cx="25" cy="25" r="20" stroke="rgba(79,70,229,0.2)" strokeWidth="6" fill="none" />
        <path d="M25 5 A20 20 0 0 1 45 25" stroke="#4f46e5" strokeWidth="6" strokeLinecap="round" fill="none" />
      </svg>
    </div>
  )
}
