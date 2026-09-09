import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * Renders an exercise's prompt.md. Content is first-party and ships in the
 * bundle; react-markdown ignores raw HTML by default, which is the behaviour
 * we want to keep even so.
 */
export function Prompt({ markdown }: { markdown: string }) {
  return (
    <div className="prose">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
    </div>
  );
}
