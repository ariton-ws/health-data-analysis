import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function GdpRecoveryReportViewer() {
  const [content, setContent] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/gdp-recovery-report')
      .then(res => res.ok ? res.text() : Promise.reject('Failed to load report'))
      .then(setContent)
      .catch(() => setError('Failed to load report'));
  }, []);

  if (error) return <div className="text-red-600">{error}</div>;
  if (!content) return <div>Loading report...</div>;

  return (
    <div className="prose max-w-none bg-white rounded-xl shadow p-6 my-8">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
} 