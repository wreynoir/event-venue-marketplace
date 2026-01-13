'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuthStore } from '@/lib/stores/auth-store'
import { venueApi, type Venue } from '@/lib/api/venues'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'

export default function VenueDashboardPage() {
  const router = useRouter()
  const { user } = useAuthStore()
  const [venues, setVenues] = useState<Venue[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadVenues()
  }, [])

  const loadVenues = async () => {
    try {
      setIsLoading(true)
      const data = await venueApi.getMyVenues()
      setVenues(data)
    } catch (err: unknown) {
      const error = err as Error
      setError(error.message || 'Failed to load venues')
    } finally {
      setIsLoading(false)
    }
  }

  // Check if user is a venue owner
  if (!user?.is_venue_owner) {
    return (
      <div className="container flex items-center justify-center min-h-[calc(100vh-4rem)] py-12">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>
              You need to be registered as a venue owner to access this page.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push('/')}>Go Home</Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const getBoroughDisplay = (borough: string) => {
    return borough.replace('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase())
  }

  return (
    <div className="container py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">My Venues</h1>
          <p className="text-muted-foreground">Manage your venue listings</p>
        </div>
        <Link href="/venue/new">
          <Button>Add New Venue</Button>
        </Link>
      </div>

      {error && (
        <div className="mb-6 p-4 text-sm text-destructive bg-destructive/10 rounded-md">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-muted-foreground">Loading venues...</p>
        </div>
      ) : venues.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <p className="text-lg text-muted-foreground mb-4">No venues yet</p>
            <p className="text-sm text-muted-foreground mb-6">
              Get started by adding your first venue
            </p>
            <Link href="/venue/new">
              <Button>Create Your First Venue</Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {venues.map((venue) => (
            <Card key={venue.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-xl">{venue.name}</CardTitle>
                    <CardDescription>
                      {getBoroughDisplay(venue.borough)}
                      {venue.neighborhood && ` • ${venue.neighborhood}`}
                    </CardDescription>
                  </div>
                  <span
                    className={`text-xs px-2 py-1 rounded-full ${
                      venue.verification_status === 'verified'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}
                  >
                    {venue.verification_status}
                  </span>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Capacity:</span>
                    <span className="font-medium">
                      {venue.capacity_min} - {venue.capacity_max} guests
                    </span>
                  </div>
                  {venue.base_price && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Starting at:</span>
                      <span className="font-medium">${venue.base_price.toLocaleString()}</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Photos:</span>
                    <span className="font-medium">{venue.photos.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Pricing Packages:</span>
                    <span className="font-medium">{venue.pricing_packages.length}</span>
                  </div>
                </div>

                <div className="pt-4 flex gap-2">
                  <Link href={`/venue/${venue.id}`} className="flex-1">
                    <Button variant="outline" className="w-full" size="sm">
                      View
                    </Button>
                  </Link>
                  <Link href={`/venue/${venue.id}/edit`} className="flex-1">
                    <Button className="w-full" size="sm">
                      Edit
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
