'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { briefsApi, type EventBrief } from '@/lib/api/briefs'
import { Button } from '@/components/ui/button'
import { CheckCircle2, Calendar, Users, MapPin, DollarSign } from 'lucide-react'

export default function BriefConfirmationPage() {
  const params = useParams()
  const router = useRouter()
  const [brief, setBrief] = useState<EventBrief | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadBrief = async () => {
      try {
        const id = parseInt(params.id as string)
        const data = await briefsApi.get(id)
        setBrief(data)
      } catch (err) {
        console.error('Failed to load brief:', err)
      } finally {
        setLoading(false)
      }
    }

    loadBrief()
  }, [params.id])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  if (!brief) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Brief not found</p>
          <Button onClick={() => router.push('/')} className="mt-4">
            Go Home
          </Button>
        </div>
      </div>
    )
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
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

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* Success message */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 dark:bg-green-900/20 mb-4">
            <CheckCircle2 className="w-8 h-8 text-green-600 dark:text-green-500" />
          </div>
          <h1 className="text-3xl font-bold mb-2">Brief Submitted!</h1>
          <p className="text-muted-foreground">
            We're matching you with the best venues in NYC
          </p>
        </div>

        {/* Brief summary */}
        <div className="bg-card border rounded-lg p-6 mb-6 space-y-4">
          <h2 className="text-xl font-semibold mb-4">Your Event Brief</h2>

          <div className="flex items-start gap-3">
            <Calendar className="w-5 h-5 text-muted-foreground mt-0.5" />
            <div>
              <p className="font-medium">{formatEventType(brief.event_type)}</p>
              <p className="text-sm text-muted-foreground">
                {formatDate(brief.date_preferred)}
                {brief.date_flexible && ' (flexible ±1 week)'}
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Users className="w-5 h-5 text-muted-foreground mt-0.5" />
            <div>
              <p className="font-medium">{brief.headcount} guests</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <MapPin className="w-5 h-5 text-muted-foreground mt-0.5" />
            <div>
              <p className="font-medium">{formatBorough(brief.borough_pref)}</p>
              {brief.neighborhood_pref && (
                <p className="text-sm text-muted-foreground">
                  {brief.neighborhood_pref}
                </p>
              )}
            </div>
          </div>

          <div className="flex items-start gap-3">
            <DollarSign className="w-5 h-5 text-muted-foreground mt-0.5" />
            <div>
              <p className="font-medium">
                Budget: ${brief.budget_min ? `${brief.budget_min} - ` : 'Up to '}
                ${brief.budget_max}
              </p>
            </div>
          </div>

          {brief.notes && (
            <div className="pt-4 border-t">
              <p className="text-sm font-medium mb-1">Additional Notes</p>
              <p className="text-sm text-muted-foreground">{brief.notes}</p>
            </div>
          )}
        </div>

        {/* Next steps */}
        <div className="bg-muted/50 rounded-lg p-6 mb-6">
          <h3 className="font-semibold mb-3">What happens next?</h3>
          <ol className="space-y-2 text-sm">
            <li className="flex items-start gap-2">
              <span className="font-semibold text-primary">1.</span>
              <span>
                We'll match your brief with venues that fit your requirements
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-semibold text-primary">2.</span>
              <span>Venues will review your brief and send personalized offers</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-semibold text-primary">3.</span>
              <span>
                You'll receive notifications when offers arrive (usually within 24
                hours)
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-semibold text-primary">4.</span>
              <span>Compare offers and book your perfect venue</span>
            </li>
          </ol>
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-3">
          <Button onClick={() => router.push(`/brief/${params.id}/matches`)} size="lg">
            View Venue Matches
          </Button>
          <Button onClick={() => router.push('/host/dashboard')} size="lg" variant="outline">
            View My Briefs
          </Button>
          <Button
            variant="ghost"
            onClick={() => router.push('/')}
            size="lg"
          >
            Go to Home
          </Button>
        </div>
      </div>
    </div>
  )
}
