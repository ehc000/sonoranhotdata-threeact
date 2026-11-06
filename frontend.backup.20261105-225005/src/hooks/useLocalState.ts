import { useState } from 'react';
export function useLocalState<T>(key: string, initial: T) {
  const [value,setValue] = useState<T>(() => {
    try { const saved = localStorage.getItem(key); return saved ? JSON.parse(saved) as T : initial; } catch { return initial; }
  });
  const update = (next: T | ((prev:T)=>T)) => setValue(prev => {
    const result = typeof next === 'function' ? (next as (prev:T)=>T)(prev) : next;
    localStorage.setItem(key,JSON.stringify(result)); return result;
  });
  return [value,update] as const;
}
