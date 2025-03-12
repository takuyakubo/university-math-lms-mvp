import AppLayout from '@/components/layout/AppLayout';
import RequireAuth from '@/components/auth/RequireAuth';

export default function ProblemsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <RequireAuth>
      <AppLayout>
        {children}
      </AppLayout>
    </RequireAuth>
  );
}