'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { briefsApi, type EventBrief } from '@/lib/api/briefs'
import { Button } from '@/components/ui/button'
import { Calendar, Users, MapPin, DollarSign, Plus } from 'lucide-react'

export default function HostDashboardPage() {
  const router = useRouter()
  const [briefs, setBriefs] = useState<EventBrief[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadBriefs = async () => {
      try {
        const data = await briefsApi.list()
        setBriefs(data.briefs)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load briefs')
      } finally {
        setLoading(false)
      }
    }

    loadBriefs()
  }, [])

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  const formatEventType = (type: string) => {
    return type
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const formatBorough = (borough: string | null) => {
    if (!borough) return 'Any borough'
    return borough
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
      case 'matched':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'booked':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400'
      case 'completed':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading your briefs...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">My Event Briefs</h1>
            <p className="text-muted-foreground">
              Track your event submissions and offers
            </p>
          </div>
          <Button onClick={() => router.push('/brief/new')} size="lg">
            <Plus className="w-5 h-5 mr-2" />
            New Brief
          </Button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-destructive/10 border border-destructive rounded-lg text-destructive">
            {error}
          </div>
        )}

        {/* Briefs list */}
        {briefs.length === 0 ? (
          <div className="text-center py-12">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-muted mb-4">
              <Calendar className="w-8 h-8 text-muted-foreground" />
            </div>
            <h2 className="text-xl font-semibold mb-2">No briefs yet</h2>
            <p className="text-muted-foreground mb-6">
              Create your first event brief to get started
            </p>
            <Button onClick={() => router.push('/brief/new')}>
              <Plus className="w-5 h-5 mr-2" />
              Create Event Brief
            </Button>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {briefs.map((brief) => (
              <div
                key={brief.id}
                className="bg-card border rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => router.push(`/brief/${brief.id}`)}
              >
                {/* Status badge */}
                <div className="flex items-center justify-between mb-4">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                      brief.status
                    )}`}
                  >
                    {brief.status.charAt(0).toUpperCase() + brief.status.slice(1)}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {formatDate(brief.created_at)}
                  </span>
                </div>

                {/* Brief details */}
                <h3 className="text-lg font-semibold mb-4">
                  {formatEventType(brief.event_type)}
                </h3>

                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm">
                    <Calendar className="w-4 h-4 text-muted-foreground" />
                    <span>{formatDate(brief.date_preferred)}</span>
                  </div>

                  <div className="flex items-center gap-2 text-sm">
                    <Users className="w-4 h-4 text-muted-foreground" />
                    <span>{brief.headcount} guests</span>
                  </div>

                  <div className="flex items-center gap-2 text-sm">
                    <MapPin className="w-4 h-4 text-muted-foreground" />
                    <span>{formatBorough(brief.borough_pref)}</span>
                  </div>

                  <div className="flex items-center gap-2 text-sm">
                    <DollarSign className="w-4 h-4 text-muted-foreground" />
                    <span>
                      {brief.budget_min ? `$${brief.budget_min} - ` : 'Up to '}$
                      {brief.budget_max}
                    </span>
                  </div>
                </div>

                {/* Footer */}
                <div className="mt-6 pt-4 border-t flex gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="flex-1"
                    onClick={(e) => {
                      e.stopPropagation()
                      router.push(`/brief/${brief.id}`)
                    }}
                  >
                    View Details
                  </Button>
                  <Button
                    size="sm"
                    className="flex-1"
                    onClick={(e) => {
                      e.stopPropagation()
                      router.push(`/brief/${brief.id}/matches`)
                    }}
                  >
                    View Matches
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
