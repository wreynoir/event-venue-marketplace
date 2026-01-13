'use client'

import Link from 'next/link'
import { useAuthStore } from '@/lib/stores/auth-store'
import { RoleSwitcher } from './role-switcher'
import { Button } from '@/components/ui/button'

export function Header() {
  const { user, isAuthenticated, logout } = useAuthStore()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-xl font-bold">VenueMatch</span>
          </Link>
        </div>

        <div className="flex items-center gap-4">
          {isAuthenticated && user ? (
            <>
              <RoleSwitcher />
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">{user.name}</span>
                <Button variant="outline" size="sm" onClick={logout}>
                  Logout
                </Button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Link href="/login">
                <Button variant="ghost" size="sm">
                  Login
                </Button>
              </Link>
              <Link href="/register">
                <Button size="sm">Sign Up</Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
