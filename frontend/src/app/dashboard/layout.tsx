import AppLayout from '@/components/layout/AppLayout';
import RequireAuth from '@/components/auth/RequireAuth';

export default function DashboardLayout({
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