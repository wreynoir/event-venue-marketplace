'use client'

import Link from 'next/link'
import { useAuthStore } from '@/lib/stores/auth-store'
import { Button } from '@/components/ui/button'

export default function Home() {
  const { user, isAuthenticated } = useAuthStore()

  return (
    <div className="container flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] py-12">
      <div className="max-w-3xl text-center space-y-8">
        <h1 className="text-5xl font-bold tracking-tight">
          Find Your Perfect NYC Venue
        </h1>
        <p className="text-xl text-muted-foreground">
          Two-sided marketplace connecting event hosts with amazing venues across all five boroughs
        </p>

        {isAuthenticated && user ? (
          <div className="space-y-4">
            <p className="text-lg">
              Welcome back, <span className="font-semibold">{user.name}</span>!
            </p>
            <div className="flex gap-4 justify-center">
              {user.is_host && (
                <Link href="/brief/new">
                  <Button size="lg">Create Event Brief</Button>
                </Link>
              )}
              {user.is_venue_owner && (
                <Link href="/venue/dashboard">
                  <Button size="lg" variant="outline">
                    Venue Dashboard
                  </Button>
                </Link>
              )}
            </div>
          </div>
        ) : (
          <div className="flex gap-4 justify-center">
            <Link href="/register">
              <Button size="lg">Get Started</Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline">
                Login
              </Button>
            </Link>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-12">
          <div className="p-6 rounded-lg border bg-card">
            <h3 className="font-semibold mb-2">60-Second Brief</h3>
            <p className="text-sm text-muted-foreground">
              Tell us about your event in under a minute
            </p>
          </div>
          <div className="p-6 rounded-lg border bg-card">
            <h3 className="font-semibold mb-2">AI-Powered Matching</h3>
            <p className="text-sm text-muted-foreground">
              Get personalized venue recommendations
            </p>
          </div>
          <div className="p-6 rounded-lg border bg-card">
            <h3 className="font-semibold mb-2">Direct Offers</h3>
            <p className="text-sm text-muted-foreground">
              Receive custom proposals from venues
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
