'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/stores/auth-store'
import { venueApi, Borough, type CreateVenueData } from '@/lib/api/venues'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select } from '@/components/ui/select'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'

export default function NewVenuePage() {
  const router = useRouter()
  const { user } = useAuthStore()
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // Form state
  const [formData, setFormData] = useState<CreateVenueData>({
    name: '',
    description: '',
    borough: Borough.MANHATTAN,
    neighborhood: '',
    address: '',
    capacity_min: 10,
    capacity_max: 100,
    base_price: undefined,
    min_spend: undefined,
    instant_book_enabled: false,
    photos: [],
    amenities: [],
    pricing_packages: [],
  })

  // Check if user is a venue owner
  if (!user?.is_venue_owner) {
    return (
      <div className="container flex items-center justify-center min-h-[calc(100vh-4rem)] py-12">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>
              You need to be registered as a venue owner to create a venue.
            </CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={() => router.push('/')}>Go Home</Button>
          </CardFooter>
        </Card>
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      // Validate
      if (formData.capacity_max < formData.capacity_min) {
        setError('Maximum capacity must be greater than or equal to minimum capacity')
        setIsLoading(false)
        return
      }

      // Create venue
      const newVenue = await venueApi.create(formData)

      // Redirect to venue dashboard
      router.push(`/venue/dashboard`)
    } catch (err: unknown) {
      const error = err as Error
      setError(error.message || 'Failed to create venue')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container max-w-2xl py-12">
      <Card>
        <CardHeader>
          <CardTitle>List Your Venue</CardTitle>
          <CardDescription>
            Tell us about your venue to get started. You can add photos, amenities, and pricing later.
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-6">
            {error && (
              <div className="p-3 text-sm text-destructive bg-destructive/10 rounded-md">
                {error}
              </div>
            )}

            {/* Basic Information */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Basic Information</h3>

              <div className="space-y-2">
                <Label htmlFor="name">Venue Name *</Label>
                <Input
                  id="name"
                  placeholder="The Grand Ballroom"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <textarea
                  id="description"
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Describe your venue, its unique features, and what makes it special..."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={4}
                />
              </div>
            </div>

            {/* Location */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Location</h3>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="borough">Borough *</Label>
                  <Select
                    id="borough"
                    value={formData.borough}
                    onChange={(e) => setFormData({ ...formData, borough: e.target.value as Borough })}
                    required
                  >
                    <option value={Borough.MANHATTAN}>Manhattan</option>
                    <option value={Borough.BROOKLYN}>Brooklyn</option>
                    <option value={Borough.QUEENS}>Queens</option>
                    <option value={Borough.BRONX}>Bronx</option>
                    <option value={Borough.STATEN_ISLAND}>Staten Island</option>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="neighborhood">Neighborhood</Label>
                  <Input
                    id="neighborhood"
                    placeholder="e.g., Williamsburg"
                    value={formData.neighborhood}
                    onChange={(e) => setFormData({ ...formData, neighborhood: e.target.value })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="address">Street Address *</Label>
                <Input
                  id="address"
                  placeholder="123 Main St, New York, NY 10001"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  required
                />
              </div>
            </div>

            {/* Capacity */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Capacity</h3>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="capacity_min">Minimum Capacity *</Label>
                  <Input
                    id="capacity_min"
                    type="number"
                    min="1"
                    placeholder="10"
                    value={formData.capacity_min}
                    onChange={(e) =>
                      setFormData({ ...formData, capacity_min: parseInt(e.target.value) || 0 })
                    }
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="capacity_max">Maximum Capacity *</Label>
                  <Input
                    id="capacity_max"
                    type="number"
                    min="1"
                    placeholder="100"
                    value={formData.capacity_max}
                    onChange={(e) =>
                      setFormData({ ...formData, capacity_max: parseInt(e.target.value) || 0 })
                    }
                    required
                  />
                </div>
              </div>
            </div>

            {/* Pricing (Optional) */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Pricing (Optional)</h3>
              <p className="text-sm text-muted-foreground">
                You can add detailed pricing packages later. For now, provide a starting price if you'd like.
              </p>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="base_price">Starting Price ($)</Label>
                  <Input
                    id="base_price"
                    type="number"
                    min="0"
                    step="0.01"
                    placeholder="1000"
                    value={formData.base_price || ''}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        base_price: e.target.value ? parseFloat(e.target.value) : undefined,
                      })
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="min_spend">Minimum Spend ($)</Label>
                  <Input
                    id="min_spend"
                    type="number"
                    min="0"
                    step="0.01"
                    placeholder="2000"
                    value={formData.min_spend || ''}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        min_spend: e.target.value ? parseFloat(e.target.value) : undefined,
                      })
                    }
                  />
                </div>
              </div>
            </div>
          </CardContent>

          <CardFooter className="flex justify-between">
            <Button type="button" variant="outline" onClick={() => router.back()}>
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Creating...' : 'Create Venue'}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
