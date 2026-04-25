import { useEffect, useState, useRef } from 'react';

export function useWebSocket(url) {
  const [lastMessage, setLastMessage] = useState(null);
  const [readyState, setReadyState] = useState(WebSocket.CONNECTING);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        setReadyState(WebSocket.OPEN);
        if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      };
      ws.onmessage = (event) => setLastMessage(JSON.parse(event.data));
      ws.onclose = () => {
        setReadyState(WebSocket.CLOSED);
        reconnectTimeoutRef.current = setTimeout(connect, 3000);
      };
      ws.onerror = (err) => console.error('WebSocket error', err);
    };
    connect();
    return () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) wsRef.current.close();
    };
  }, [url]);

  return { lastMessage, readyState };
}
