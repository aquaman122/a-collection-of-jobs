"use client";

import { IJobs } from "@/app/types/job";
import { supabase } from "@/lib/supabase/client";
import { useCallback, useEffect, useRef, useState } from "react";

export default function JobsCard () {
  const [jobs, setJobs] = useState<IJobs[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const observerRef = useRef<HTMLDivElement | null>(null);
  const page = useRef(0);
  const pageSize = 50

  const deduplicateJobs = (jobs: IJobs[]): IJobs[] => {
    const map = new Map<string, IJobs>();
    jobs.forEach((job) => {
      if (!map.has(job.link)) {
        map.set(job.link, job);
      }
    });
    return Array.from(map.values());
  };

  const fetchJobs = useCallback(async () => {
    setLoading(true);

    const { data, error } = await supabase
      .from("job_posts")
      .select("*")
      .order("posted_date", { ascending: false })
      .range(page.current * pageSize, (page.current + 1) * pageSize - 1)

    if (error) {
      setLoading(false)
      return;
    }

    if (data.length < pageSize) setHasMore(false)

    setJobs((prev) => deduplicateJobs([...prev, ...data]))
    page.current += 1
    setLoading(false)
  }, []);

  useEffect(() => {
    if (!hasMore || loading) return;
  
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        fetchJobs();
      }
    }, { threshold: 1.0 });
  
    const currentRef = observerRef.current;
    if (currentRef) observer.observe(currentRef);
  
    return () => {
      if (currentRef) observer.unobserve(currentRef);
    };
  }, [fetchJobs, hasMore, loading]);

  return (
    <div className="grid gap-4">
      {jobs.map((job, idx) => (
        <div key={`${job.link}-${idx}`} className="border p-4 rounded shadow-sm">
          <h2 className="text-xl font-bold">{job.title}</h2>
          <p className="text-gray-600">{job.company}</p>
          <p className="text-sm">{job.career} | {job.location}</p>
          <p className="text-xs text-gray-400">{job.source} | {job.posted_date}</p>
          <a
            href={job.link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 underline mt-2 inline-block"
          >
            자세히 보기
          </a>
        </div>
      ))}
      {hasMore && (
        <div ref={observerRef} className="h-10" />
      )}
    </div>
  );
};